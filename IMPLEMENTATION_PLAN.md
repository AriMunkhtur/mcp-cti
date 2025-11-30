# Dashboard Improvement Plan

## Goal
Enhance the MCP CTI Dashboard with graphs, threat scores, and a better UI to provide more actionable insights.

## User Review Required
> [!NOTE]
> I will be adding synthetic "severity" and "score" fields to the threat data for demonstration purposes, as the basic OTX feed might not always provide granular scores for every indicator.

## Proposed Changes

### Backend (`mcp_server.py`)
#### [MODIFY] [mcp_server.py](file:///c:/Users/HiTech/Documents/mcp-cti/mcp_server.py)
- Update `Threat` model to include:
    - `severity`: str (High, Medium, Low)
    - `score`: float (0.0 - 10.0)
- Update `SAMPLE_THREATS` with these new fields.
- Update `normalize_pulses_to_indicators` to assign a mock severity/score (randomized or based on simple heuristics) since the raw OTX data in this simple demo might not have it normalized.

### Frontend (`dashboard.py`)
#### [MODIFY] [dashboard.py](file:///c:/Users/HiTech/Documents/mcp-cti/dashboard.py)
- **Metrics Row**: Add `st.metric` for Total Threats, Avg Risk Score, Critical Threats.
- **Visualizations**:
    - Bar chart of Threats by Type.
    - Pie/Donut chart of Threats by Severity.
- **Data Grid**: Use `st.dataframe` with column configuration (progress bar for score) instead of simple `st.table`.
- **Layout**: Use `st.columns` for better arrangement.

## Verification Plan

### Automated Tests
- None (Visual verification required).

### Manual Verification
1. Run `uvicorn mcp_server:app --reload`
2. Run `streamlit run dashboard.py`
3. Verify the dashboard shows:
    - 3 Key Metrics at the top.
    - A chart showing threat distribution.
    - A data table with a "Score" column.
