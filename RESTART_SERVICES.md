# 🚀 Restart Services with Live OTX Feed

## What's New

I've enhanced your CTI dashboard with:

### 🎯 Backend Improvements (`mcp_server.py`)
- ✅ **Live OTX Integration** - Your API key is now configured
- ✅ **Smart Threat Scoring** - Based on community references, indicator types, and tags
- ✅ **Enhanced Data** - Tags, creation dates, reference counts
- ✅ **New `/stats` Endpoint** - For advanced analytics

### 🎨 Dashboard Enhancements (`dashboard.py`)
- ✅ **Tag Cloud** - See most common threat tags
- ✅ **Timeline View** - Threats over time
- ✅ **Score Distribution** - Histogram of risk scores
- ✅ **Reference Analysis** - Community engagement vs risk
- ✅ **Advanced Filters** - Filter by severity, type, and score
- ✅ **CSV Export** - Download filtered threat data
- ✅ **4 Metric Cards** - Total, Avg Score, Critical, High counts

---

## 📋 How to Restart

### Step 1: Stop Current Services

In your terminal, press `Ctrl+C` to stop:
1. The Streamlit dashboard (if running)
2. The uvicorn server (if running)

### Step 2: Start the MCP Server

```powershell
.\.venv\Scripts\python.exe -m uvicorn mcp_server:app --host 0.0.0.0 --port 9000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### Step 3: Start the Dashboard (New Terminal)

Open a **new PowerShell terminal** in the same directory and run:

```powershell
.\.venv\Scripts\streamlit.exe run dashboard.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://10.0.0.95:8501
```

### Step 4: Open in Browser

Navigate to: **http://localhost:8501** (or whatever port Streamlit shows)

---

## 🔍 What You'll See

1. **4 Metrics** at the top showing threat counts and scores
2. **Severity & Type Charts** - Visual breakdown
3. **3 Analysis Tabs**:
   - 📊 Score Analysis - Distribution and correlation
   - 🏷️ Tag Intelligence - Most common threat tags
   - 📅 Timeline - Threats over time
4. **Filterable Table** - With severity, type, and score filters
5. **CSV Export** - Download button for filtered data

---

## 🎯 Live OTX Data

Your OTX API key is configured in `.env`. The dashboard will now show:
- Real threat intelligence from AlienVault OTX
- Filtered by your assets in `assets.json`
- Scored based on community engagement and threat type
- Sorted by risk score (highest first)

---

## 🛠️ Troubleshooting

**If you see "No threats found":**
1. Check that your OTX API key is valid
2. Verify `assets.json` has entries
3. The server might be filtering too aggressively - check the server logs

**If charts don't load:**
- Refresh the page (Streamlit sometimes needs a refresh)
- Check browser console for errors

**Port already in use:**
- Streamlit will auto-increment (8501 → 8502 → 8503)
- Use whatever port it shows in the terminal
