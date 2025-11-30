# MCP CTI Dashboard - Complete Project Context

## Project Overview

This is a **Cyber Threat Intelligence (CTI) Dashboard** that pulls live threat data from AlienVault OTX (Open Threat Exchange) and displays it in an interactive web interface. The system filters threats based on your specific assets and allows you to focus on threats relevant to your organization or research interests.

---

## Technology Stack

### Backend
- **Language**: Python 3.14
- **Framework**: FastAPI (REST API server)
- **Server**: Uvicorn (ASGI server)
- **Port**: 9000

### Frontend
- **Framework**: Streamlit (Python web framework)
- **Visualization**: Plotly (interactive charts)
- **Data Processing**: Pandas
- **Port**: 8501

### Data Source
- **API**: AlienVault OTX (Open Threat Exchange)
- **API Key**: Configured in `.env` file
- **Data Format**: JSON

---

## Project Structure

```
mcp-cti/
├── .env                    # Environment variables (API keys)
├── .env.example           # Template for environment variables
├── assets.json            # Asset inventory (user-editable)
├── mcp_server.py          # Backend API server
├── dashboard.py           # Frontend Streamlit dashboard
├── requirements.txt       # Python dependencies
├── BEGINNERS_GUIDE.md     # User documentation
├── WALKTHROUGH.md         # Technical walkthrough
├── IMPLEMENTATION_PLAN.md # Original implementation plan
├── RESTART_SERVICES.md    # Service restart instructions
└── .venv/                 # Python virtual environment
```

---

## How It Works

### Data Flow

1. **OTX API** → Provides threat intelligence pulses
2. **MCP Server** (`mcp_server.py`) → Fetches, normalizes, scores, and filters threats
3. **Dashboard** (`dashboard.py`) → Displays threats with interactive visualizations
4. **User** → Interacts with dashboard, manages assets, applies filters

### Architecture Diagram

```
┌─────────────────┐
│  AlienVault OTX │ (External API)
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  mcp_server.py  │ (Port 9000)
│   - Fetch data  │
│   - Score       │
│   - Filter      │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  dashboard.py   │ (Port 8501)
│   - Visualize   │
│   - Filter UI   │
│   - Export      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      User       │ (Web Browser)
└─────────────────┘
```

---

## Key Features

### 1. Live Threat Intelligence
- Fetches up to 100 recent threat pulses from OTX
- Updates automatically when server is running
- Real-time data from global security community

### 2. Smart Threat Scoring (0-10 scale)
The system calculates risk scores based on:
- **Community References**: More subscribers = higher score
- **Indicator Type**: CVEs, malware, exploits get boosted
- **Threat Tags**: APT, ransomware, zero-day increase severity
- **Base Score**: 5.0 (adjusted up or down)

**Scoring Algorithm:**
```python
score = 5.0  # Base
if references > 100: score += 2.0
if "cve" in type: score += 1.5
if "ransomware" in tags: score += 0.5
# Cap at 10.0
```

### 3. Severity Classification
- **Critical** (9.0-10.0): Red - Immediate action required
- **High** (6.5-8.9): Orange - Address soon
- **Medium** (4.0-6.4): Yellow - Monitor
- **Low** (0.0-3.9): Green - Informational

### 4. Asset-Based Filtering
The system only shows threats relevant to YOUR assets:
- Matches software names (e.g., "PHP", "WordPress")
- Matches versions (e.g., "8.1", "6.2.0")
- Matches tags
- Always includes CVEs (generally relevant)

**Example:**
```json
{
  "name": "Web Server",
  "software": "PHP",
  "version": "8.1"
}
```
→ Shows threats mentioning "PHP" or "8.1"

### 5. Interactive Dashboard

#### Top Metrics (4 Cards)
- Total Threats
- Average Risk Score
- Critical Count
- High Count

#### Main Charts
- **Severity Distribution**: Bar chart with color coding
- **Threat Types**: Donut chart showing indicator types

#### Analysis Tabs
1. **Score Analysis**
   - Score distribution histogram
   - References vs Score scatter plot

2. **Tag Intelligence**
   - Tag cloud (top 15 tags)
   - Top 3 tags with counts

3. **Timeline**
   - Line chart of threats over time
   - Recent threats list (last 5)

#### Sidebar Controls
- **Asset Management**: Add/delete assets on the fly
- **Country/Region Filter**: Focus on specific countries (e.g., "Mongolia")
- **Campaign/Actor Filter**: Track specific threat actors (e.g., "APT28")
- **Keywords Filter**: Search for attack types (e.g., "ransomware")
- **Display Controls**: Show/hide low severity, adjust max threats

#### Threat Table
Columns:
- Severity (color-coded badge)
- Risk Score (progress bar)
- Threat Name
- Type (CVE, FileHash, Domain, etc.)
- Indicator Value
- Tags (list)
- Created Date
- References (community count)

Filters:
- Severity multi-select
- Type multi-select
- Minimum risk score slider

#### Export
- Download filtered threats as CSV
- Timestamped filename
- All columns included

---

## API Endpoints

### Backend (Port 9000)

#### GET `/threats`
Returns filtered threat list

**Response:**
```json
[
  {
    "type": "cve",
    "value": "CVE-2024-1234",
    "threat_name": "Critical RCE Vulnerability",
    "source": "otx",
    "severity": "Critical",
    "score": 9.5,
    "tags": ["rce", "exploit"],
    "created": "2024-11-20",
    "references": 150
  }
]
```

#### GET `/stats`
Returns threat statistics

**Response:**
```json
{
  "total_threats": 38,
  "severity_distribution": {
    "Critical": 5,
    "High": 12,
    "Medium": 18,
    "Low": 3
  },
  "type_distribution": {
    "cve": 15,
    "FileHash": 10,
    "domain": 8,
    "IPv4": 5
  },
  "top_tags": {
    "ransomware": 8,
    "phishing": 6,
    "apt": 4
  },
  "avg_score": 6.8,
  "critical_count": 5
}
```

#### GET `/docs`
FastAPI auto-generated API documentation (Swagger UI)

---

## Configuration Files

### `.env`
```bash
OTX_API_KEY=7fbdde078db43d502644ced20988143dde9a3954278a83f0a45e277c8c705944
MCP_API_URL=http://localhost:9000/threats
# ANTHROPIC_API_KEY=optional_for_llm_summaries
```

### `assets.json`
```json
[
  { "name": "Web Server", "software": "PHP", "version": "8.1" },
  { "name": "Database", "software": "MySQL", "version": "5.7" },
  { "name": "CMS", "software": "WordPress", "version": "6.2.0" },
  { "name": "OS", "software": "Ubuntu", "version": "22.04" },
  { "name": "Web Server", "software": "Nginx", "version": "1.18.0" },
  { "name": "Runtime", "software": "Python", "version": "3.10" },
  { "name": "Database", "software": "PostgreSQL", "version": "14" }
]
```

### `requirements.txt`
```
fastapi
uvicorn[standard]
requests
python-dotenv
anthropic
streamlit
pandas
plotly
```

---

## Running the System

### Prerequisites
- Python 3.14 (or 3.10+)
- Virtual environment created
- Dependencies installed

### Start Backend Server
```powershell
.\.venv\Scripts\python.exe -m uvicorn mcp_server:app --host 0.0.0.0 --port 9000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Start Dashboard
```powershell
.\.venv\Scripts\streamlit.exe run dashboard.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://10.0.0.95:8501
```

### Access Points
- **Dashboard**: http://localhost:8501
- **API Threats**: http://localhost:9000/threats
- **API Stats**: http://localhost:9000/stats
- **API Docs**: http://localhost:9000/docs

---

## Development History

### Initial State
- Basic MCP server with sample threats
- Simple Streamlit dashboard with table view
- No scoring, no filtering, no visualizations

### Enhancements Made

#### Phase 1: Basic Improvements
- Added severity and score fields to Threat model
- Updated sample data with realistic values
- Added basic charts (severity bar chart, type pie chart)
- Added metrics cards

#### Phase 2: Advanced Features
- Implemented smart threat scoring algorithm
- Added tag extraction from OTX pulses
- Added timeline data (creation dates)
- Added reference tracking (community engagement)
- Created `/stats` endpoint

#### Phase 3: Dashboard Enhancements
- Switched from Altair to Plotly (Python 3.14 compatibility)
- Added 3 analysis tabs (Score, Tags, Timeline)
- Added tag cloud visualization
- Added score distribution histogram
- Added references vs score scatter plot
- Added timeline line chart
- Added recent threats list

#### Phase 4: Interactive Controls
- Added sidebar with configuration panel
- Implemented asset management (add/delete assets)
- Added country/region filter
- Added campaign/actor filter
- Added keywords filter
- Added display controls (show/hide low severity, max threats)
- Added CSV export functionality

#### Phase 5: Bug Fixes
- Fixed TypeError with references field (was list, expected int)
- Added safety checks for optional fields (tags, created, references)
- Made dashboard crash-proof when server is down
- Fixed column configuration for missing fields

---

## Technical Challenges Solved

### 1. Python 3.14 Compatibility
**Problem**: Altair library had TypedDict issues with Python 3.14  
**Solution**: Switched to Plotly for all visualizations

### 2. OTX Data Inconsistency
**Problem**: References field sometimes returned as list instead of int  
**Solution**: Added type checking and conversion:
```python
if isinstance(references, list):
    references = len(references)
references = int(references) if references else 0
```

### 3. Missing Fields
**Problem**: Dashboard crashed when optional fields were missing  
**Solution**: Added existence checks before accessing columns:
```python
if "tags" in df.columns:
    # Process tags
```

### 4. Process Management
**Problem**: Couldn't programmatically restart Streamlit  
**Solution**: Provided manual restart instructions and made dashboard auto-reload on file changes

---

## Use Cases

### 1. Web Developer
**Scenario**: Protect production web applications  
**Assets**: PHP, MySQL, WordPress, Nginx  
**Workflow**:
1. Add assets to dashboard
2. Check daily for Critical/High threats
3. Update software when vulnerabilities found
4. Export monthly reports

### 2. Security Researcher
**Scenario**: Track APT groups  
**Focus**: Campaign/Actor filter  
**Workflow**:
1. Filter by "APT28, APT29, Lazarus"
2. Analyze timeline for activity patterns
3. Study tags to understand TTPs
4. Export data for research

### 3. Regional Organization
**Scenario**: Monitor threats to Mongolia  
**Focus**: Country/Region filter  
**Workflow**:
1. Filter by "Mongolia"
2. Check if threat activity is increasing
3. Identify attack methods being used
4. Share Critical threats with IT team

---

## Data Model

### Threat Object
```python
{
    "type": str,           # Indicator type (cve, FileHash, domain, etc.)
    "value": str,          # Indicator value (CVE-2024-1234, malware.com, etc.)
    "threat_name": str,    # Human-readable threat name
    "source": str,         # Data source (otx, sample)
    "severity": str,       # Critical, High, Medium, Low
    "score": float,        # Risk score 0.0-10.0
    "tags": List[str],     # Keywords (ransomware, apt, phishing, etc.)
    "created": str,        # ISO date string (2024-11-20)
    "references": int      # Community reference count
}
```

### Asset Object
```python
{
    "name": str,      # Asset name (Web Server, Database, etc.)
    "software": str,  # Software name (PHP, MySQL, etc.)
    "version": str    # Version number (8.1, 5.7, etc.)
}
```

---

## Security Considerations

### API Key Management
- OTX API key stored in `.env` (not committed to git)
- `.env.example` provided as template
- Key has read-only access to OTX

### Data Privacy
- No sensitive data stored
- All data from public OTX feed
- No user authentication required (local use)

### Network Security
- Server binds to 0.0.0.0 (all interfaces)
- Intended for local/internal network use
- No HTTPS (use reverse proxy for production)

---

## Future Enhancement Ideas

1. **Real-time Updates**: WebSocket for live threat feed
2. **Alerting**: Email/Slack notifications for Critical threats
3. **Historical Analysis**: Store threats in database, track trends
4. **MITRE ATT&CK Mapping**: Link threats to attack techniques
5. **Multi-source Feeds**: Add more threat intelligence sources
6. **Custom Scoring**: User-defined scoring rules
7. **Threat Correlation**: Identify related threats
8. **SIEM Integration**: Export to Splunk, ELK, etc.
9. **Authentication**: Add user login for multi-user environments
10. **Automated Response**: Trigger security tools based on threats

---

## Troubleshooting

### Server Returns 500 Error
**Cause**: Server crashed or not running  
**Fix**: Check server terminal for errors, restart server

### No Threats Showing
**Causes**:
1. OTX API key invalid
2. No assets configured
3. Filters too restrictive

**Fixes**:
1. Verify API key in `.env`
2. Add assets in sidebar
3. Clear filters

### Dashboard Won't Load
**Cause**: Streamlit not running  
**Fix**: Start Streamlit with `streamlit run dashboard.py`

### Charts Not Displaying
**Cause**: Missing data fields  
**Fix**: Dashboard now handles this gracefully, should show "No data available"

---

## Performance Metrics

### Current Performance
- **API Response Time**: ~2-3 seconds (OTX fetch)
- **Dashboard Load Time**: ~3-4 seconds
- **Threats Processed**: Up to 100 pulses
- **Indicators Extracted**: Varies (typically 200-500)
- **Filtered Results**: Typically 20-50 threats

### Optimization Opportunities
- Cache OTX responses (reduce API calls)
- Database storage (faster queries)
- Pagination (handle more threats)
- Async processing (parallel data fetching)

---

## Documentation Files

1. **BEGINNERS_GUIDE.md**: User-friendly explanation for non-technical users
2. **WALKTHROUGH.md**: Technical walkthrough of features
3. **IMPLEMENTATION_PLAN.md**: Original development plan
4. **RESTART_SERVICES.md**: Service restart instructions
5. **PROJECT_CONTEXT.md**: This file - complete project overview

---

## Key Takeaways

### What This Project Does
✅ Fetches live cyber threat intelligence  
✅ Filters threats by your specific assets  
✅ Scores threats by risk level  
✅ Visualizes data with interactive charts  
✅ Allows custom filtering by country, actor, keywords  
✅ Exports data for reporting  

### What Makes It Unique
🎯 Asset-based filtering (only relevant threats)  
🧠 Smart scoring algorithm (not just random numbers)  
🌍 Geo-filtering (focus on specific regions)  
🏷️ Tag intelligence (understand attack trends)  
📊 Multiple visualization types (charts, tables, timelines)  
⚙️ Interactive controls (manage everything from UI)  

### Technologies Demonstrated
- REST API development (FastAPI)
- Web dashboard creation (Streamlit)
- Data visualization (Plotly)
- External API integration (OTX)
- Data processing (Pandas)
- Python async/await patterns
- Environment configuration
- JSON data handling

---

## Quick Reference Commands

### Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run
```powershell
# Terminal 1 - Backend
.\.venv\Scripts\python.exe -m uvicorn mcp_server:app --host 0.0.0.0 --port 9000 --reload

# Terminal 2 - Frontend
.\.venv\Scripts\streamlit.exe run dashboard.py
```

### Test
```powershell
# Test API
curl http://localhost:9000/threats

# Test with Python
.\.venv\Scripts\python.exe -c "import requests; print(requests.get('http://localhost:9000/threats').json())"
```

### Stop
```powershell
# Kill all processes
Get-Process streamlit -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process python | Where-Object {$_.Path -like "*mcp-cti\.venv*"} | Stop-Process -Force
```

---

## Contact & Support

For questions about this project, refer to:
- Code comments in `mcp_server.py` and `dashboard.py`
- Documentation files in project root
- FastAPI docs at http://localhost:9000/docs
- Streamlit docs at https://docs.streamlit.io

---

**Last Updated**: 2024-11-24  
**Version**: 2.0  
**Status**: Production Ready ✅
