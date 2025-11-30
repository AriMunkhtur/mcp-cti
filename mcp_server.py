from typing import List, Dict, Any, Optional
import os
import json
from pathlib import Path
from datetime import datetime
import re

import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

OTX_API_KEY = os.getenv("OTX_API_KEY")
BASE_DIR = Path(__file__).parent
ASSETS_FILE = BASE_DIR / "assets.json"


class Threat(BaseModel):
    type: str
    value: str
    threat_name: str
    source: str
    severity: str
    score: float
    tags: Optional[List[str]] = []
    created: Optional[str] = None
    references: Optional[int] = 0


SAMPLE_THREATS = [
    {"type": "software", "value": "PHP 8.1", "threat_name": "Exploit targeting PHP 8.1 in Web Server", "source": "sample", "severity": "High", "score": 8.5, "tags": ["exploit", "web"], "created": "2024-01-15", "references": 5},
    {"type": "cve", "value": "CVE-2023-1234", "threat_name": "RCE against MySQL plugin", "source": "sample", "severity": "Critical", "score": 9.8, "tags": ["rce", "database"], "created": "2024-01-10", "references": 12},
    {"type": "software", "value": "WordPress 6.2.0", "threat_name": "WordPress 6.2.0 plugin vuln exploited", "source": "sample", "severity": "Medium", "score": 5.5, "tags": ["cms", "plugin"], "created": "2024-01-20", "references": 3},
]


def get_otx_pulses(api_key: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Fetch recent pulses from AlienVault OTX. If the API call fails, return an empty list.

    This is intentionally minimal for educational purposes.
    """
    if not api_key:
        return []

    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": api_key}
    params = {"limit": limit, "page": 1}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        if isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"OTX API Error: {e}")
        return []


def calculate_threat_score(pulse: Dict[str, Any], indicator: Dict[str, Any]) -> float:
    """Calculate a threat score based on various factors."""
    score = 5.0  # Base score
    
    # Boost score based on references/subscribers
    references = pulse.get("subscriber_count", 0) or pulse.get("references", 0) or 0
    # Handle if references is a list
    if isinstance(references, list):
        references = len(references)
    references = int(references) if references else 0
    
    if references > 100:
        score += 2.0
    elif references > 50:
        score += 1.5
    elif references > 10:
        score += 1.0
    
    # Boost based on indicator type
    ind_type = (indicator.get("type") or indicator.get("indicator_type") or "").lower()
    if "cve" in ind_type:
        score += 1.5
    elif "malware" in ind_type or "trojan" in ind_type:
        score += 1.0
    elif "exploit" in ind_type:
        score += 1.2
    
    # Boost based on tags
    tags = pulse.get("tags", []) or []
    critical_tags = ["apt", "ransomware", "zero-day", "critical", "exploit-kit"]
    for tag in tags:
        if any(ct in tag.lower() for ct in critical_tags):
            score += 0.5
    
    # Cap at 10.0
    return min(round(score, 1), 10.0)


def determine_severity(score: float) -> str:
    """Map score to severity level."""
    if score >= 8.5:
        return "Critical"
    elif score >= 6.5:
        return "High"
    elif score >= 4.0:
        return "Medium"
    else:
        return "Low"


def normalize_pulses_to_indicators(pulses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    
    for p in pulses:
        name = p.get("name") or "unknown"
        created = p.get("created") or p.get("modified") or datetime.now().isoformat()
        tags = p.get("tags", []) or []
        references = p.get("subscriber_count", 0) or p.get("references", 0) or 0
        # Handle if references is a list
        if isinstance(references, list):
            references = len(references)
        references = int(references) if references else 0
        
        indicators = p.get("indicators", []) or []
        
        for ind in indicators:
            ind_type = ind.get("type") or ind.get("indicator_type") or "indicator"
            value = ind.get("indicator") or ind.get("value") or str(ind)
            
            # Calculate dynamic score
            score = calculate_threat_score(p, ind)
            severity = determine_severity(score)
            
            normalized.append({
                "type": ind_type,
                "value": value[:100],  # Truncate long values
                "threat_name": name[:150],
                "source": "otx",
                "severity": severity,
                "score": score,
                "tags": tags[:5],  # Limit tags
                "created": created.split("T")[0] if "T" in created else created,
                "references": references
            })
        
        # If no indicators, create a pulse-level entry
        if not indicators:
            score = calculate_threat_score(p, {})
            severity = determine_severity(score)
            normalized.append({
                "type": "pulse",
                "value": name[:100],
                "threat_name": name[:150],
                "source": "otx",
                "severity": severity,
                "score": score,
                "tags": tags[:5],
                "created": created.split("T")[0] if "T" in created else created,
                "references": references
            })
    
    return normalized


def load_assets() -> List[Dict[str, Any]]:
    if not ASSETS_FILE.exists():
        return []
    try:
        with open(ASSETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def filter_threats_by_assets(threats: List[Dict[str, Any]], assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not assets:
        return threats  # Return all if no assets defined
    
    filtered: List[Dict[str, Any]] = []
    for t in threats:
        t_name = (t.get("threat_name") or "").lower()
        t_value = (t.get("value") or "").lower()
        t_tags = [tag.lower() for tag in (t.get("tags") or [])]
        
        matched = False
        for a in assets:
            name = (a.get("name") or "").lower()
            software = (a.get("software") or "").lower()
            version = (a.get("version") or "").lower()
            
            # Check in threat name and value
            if software and (software in t_name or software in t_value):
                matched = True
            if version and version in t_name:
                matched = True
            
            # Check in tags
            if software and any(software in tag for tag in t_tags):
                matched = True
            
            # Check for CVEs
            if "cve" in t.get("type", "").lower():
                # CVEs are generally relevant
                matched = True
            
            if matched:
                filtered.append(t)
                break
    
    return filtered


app = FastAPI(title="MCP CTI Server")


@app.get("/threats", response_model=List[Threat])
def get_threats():
    """Get threats filtered by assets."""
    pulses = get_otx_pulses(OTX_API_KEY, limit=100)
    if pulses:
        indicators = normalize_pulses_to_indicators(pulses)
    else:
        indicators = SAMPLE_THREATS

    assets = load_assets()
    if assets:
        relevant = filter_threats_by_assets(indicators, assets)
    else:
        relevant = indicators[:50]  # Limit to 50 if no filtering

    # Sort by score descending
    relevant.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    return relevant[:100]  # Return top 100


@app.get("/stats")
def get_stats():
    """Get threat statistics."""
    pulses = get_otx_pulses(OTX_API_KEY, limit=100)
    if pulses:
        indicators = normalize_pulses_to_indicators(pulses)
    else:
        indicators = SAMPLE_THREATS
    
    assets = load_assets()
    if assets:
        relevant = filter_threats_by_assets(indicators, assets)
    else:
        relevant = indicators[:50]
    
    # Calculate stats
    severity_counts = {}
    type_counts = {}
    tag_counts = {}
    
    for threat in relevant:
        # Severity
        sev = threat.get("severity", "Unknown")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        # Type
        t_type = threat.get("type", "Unknown")
        type_counts[t_type] = type_counts.get(t_type, 0) + 1
        
        # Tags
        for tag in threat.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Get top tags
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "total_threats": len(relevant),
        "severity_distribution": severity_counts,
        "type_distribution": type_counts,
        "top_tags": dict(top_tags),
        "avg_score": round(sum(t.get("score", 0) for t in relevant) / len(relevant), 2) if relevant else 0,
        "critical_count": severity_counts.get("Critical", 0)
    }
