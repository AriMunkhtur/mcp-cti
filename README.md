# MCP CTI Minimal Demo

This is a minimal educational demo showing how a Model Context Protocol (MCP) server can normalize CTI feeds and filter them against a small asset inventory, then expose results to a Streamlit dashboard.

Demo video : 

Files:
- `mcp_server.py` — FastAPI server exposing `GET /threats` on port 9000 (default via uvicorn).
- `dashboard.py` — Streamlit app that calls the MCP server and shows relevant threats.
- `assets.json` — Sample local asset inventory used to filter threats.
- `.env.example` — Environment variable examples.

Quick start (Windows PowerShell):

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in `OTX_API_KEY` if you want live data.

3. Start the MCP FastAPI server:

```powershell
uvicorn mcp_server:app --host 0.0.0.0 --port 9000
```

4. (Optional) Streamlit dashboard

To run the Streamlit dashboard you must install `streamlit` separately (it pulls heavy binary deps like
`pyarrow` which may require build tools on Windows). Install it only if you want the UI:

```powershell
.\.venv\Scripts\pip.exe install streamlit
.\.venv\Scripts\streamlit.exe run dashboard.py
```

If you prefer to skip installing `pyarrow` or other heavy build deps, you can still run the FastAPI server
and fetch the JSON directly from `http://localhost:9000/threats`.

Notes:
- If you don't provide an `OTX_API_KEY`, the server will return a small set of sample threats.
- Anthropic integration in the dashboard is optional and used only if `ANTHROPIC_API_KEY` is set and the `anthropic` package is available.
