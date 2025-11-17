from typing import List, Dict, Any
import os
import json
from pathlib import Path

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


SAMPLE_THREATS = [
    {"type": "software", "value": "PHP 8.1", "threat_name": "Exploit targeting PHP 8.1 in Web Server", "source": "sample"},
    {"type": "cve", "value": "CVE-2023-1234", "threat_name": "RCE against MySQL plugin", "source": "sample"},
    {"type": "software", "value": "WordPress 6.2.0", "threat_name": "WordPress 6.2.0 plugin vuln exploited", "source": "sample"},
]


def get_otx_pulses(api_key: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch recent pulses from AlienVault OTX. If the API call fails, return an empty list.

    This is intentionally minimal for educational purposes.
    """
    if not api_key:
        return []

    url = "https://otx.alienvault.com/api/v1/pulses"
    headers = {"X-OTX-API-KEY": api_key}
    params = {"limit": limit}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


def normalize_pulses_to_indicators(pulses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for p in pulses:
        name = p.get("name") or p.get("pulse_info", {}).get("name") or "unknown"
        indicators = p.get("indicators") or p.get("pulse_info", {}).get("indicators") or []
        for ind in indicators:
            t = ind.get("type") or ind.get("indicator_type") or "indicator"
            v = ind.get("indicator") or ind.get("value") or str(ind)
            normalized.append({"type": t, "value": v, "threat_name": name, "source": "otx"})
        if not indicators:
            normalized.append({"type": "pulse", "value": name, "threat_name": name, "source": "otx"})
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
        return []
    filtered: List[Dict[str, Any]] = []
    for t in threats:
        t_name = (t.get("threat_name") or "").lower()
        t_value = (t.get("value") or "").lower()
        matched = False
        for a in assets:
            name = (a.get("name") or "").lower()
            software = (a.get("software") or "").lower()
            version = (a.get("version") or "").lower()
            if name and name in t_name:
                matched = True
            if software and (software in t_name or software in t_value):
                matched = True
            if version and version in t_name:
                matched = True
            if matched:
                filtered.append(t)
                break
    return filtered


app = FastAPI(title="MCP CTI Server")


@app.get("/threats", response_model=List[Threat])
def get_threats():
    pulses = get_otx_pulses(OTX_API_KEY, limit=50)
    if pulses:
        indicators = normalize_pulses_to_indicators(pulses)
    else:
        indicators = SAMPLE_THREATS

    assets = load_assets()
    if assets:
        relevant = filter_threats_by_assets(indicators, assets)
    else:
        relevant = indicators

    return relevant
