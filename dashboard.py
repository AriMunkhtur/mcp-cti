import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

load_dotenv()

API_URL = os.getenv("MCP_API_URL", "http://localhost:9000/threats")
STATS_URL = os.getenv("MCP_API_URL", "http://localhost:9000/stats").replace("/threats", "/stats")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ASSETS_FILE = Path("assets.json")


def load_assets():
    """Load assets from JSON file."""
    if ASSETS_FILE.exists():
        try:
            with open(ASSETS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_assets(assets):
    """Save assets to JSON file."""
    try:
        with open(ASSETS_FILE, "w", encoding="utf-8") as f:
            json.dump(assets, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Failed to save assets: {e}")
        return False


def fetch_threats(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch threats: {e}")
        return []


def fetch_stats(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return None


def create_tag_cloud_chart(df):
    """Create a tag cloud visualization."""
    # Safety check for tags column
    if "tags" not in df.columns:
        return None
    
    all_tags = []
    for tags in df["tags"]:
        if isinstance(tags, list):
            all_tags.extend(tags)
    
    if not all_tags:
        return None
    
    tag_counts = Counter(all_tags)
    top_tags = tag_counts.most_common(15)
    
    if not top_tags:
        return None
    
    tag_df = pd.DataFrame(top_tags, columns=["Tag", "Count"])
    
    fig = px.bar(
        tag_df,
        x="Count",
        y="Tag",
        orientation='h',
        title="Top Threat Tags",
        color="Count",
        color_continuous_scale="Reds"
    )
    fig.update_layout(height=400, showlegend=False)
    return fig


def create_timeline_chart(df):
    """Create a timeline of threats by creation date."""
    if "created" not in df.columns or df["created"].isna().all():
        return None
    
    df_timeline = df.copy()
    df_timeline["created"] = pd.to_datetime(df_timeline["created"], errors='coerce')
    df_timeline = df_timeline.dropna(subset=["created"])
    
    if len(df_timeline) == 0:
        return None
    
    # Group by date and severity
    timeline_data = df_timeline.groupby([df_timeline["created"].dt.date, "severity"]).size().reset_index(name="count")
    timeline_data.columns = ["date", "severity", "count"]
    
    color_map = {
        "Critical": "#dc2626",
        "High": "#ea580c",
        "Medium": "#f59e0b",
        "Low": "#10b981"
    }
    
    fig = px.line(
        timeline_data,
        x="date",
        y="count",
        color="severity",
        color_discrete_map=color_map,
        title="Threat Timeline",
        markers=True
    )
    fig.update_layout(height=350)
    return fig


def create_score_distribution(df):
    """Create a histogram of threat scores."""
    fig = px.histogram(
        df,
        x="score",
        nbins=20,
        title="Threat Score Distribution",
        color_discrete_sequence=["#6366f1"]
    )
    fig.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Count",
        height=300
    )
    return fig


def create_reference_vs_score(df):
    """Create a scatter plot of references vs score."""
    if "references" not in df.columns:
        return None
    
    fig = px.scatter(
        df,
        x="references",
        y="score",
        color="severity",
        size="references",
        hover_data=["threat_name", "type"],
        title="Community References vs Risk Score",
        color_discrete_map={
            "Critical": "#dc2626",
            "High": "#ea580c",
            "Medium": "#f59e0b",
            "Low": "#10b981"
        }
    )
    fig.update_layout(height=350)
    return fig


def main():
    st.set_page_config(page_title="MCP CTI Dashboard", layout="wide", page_icon="🛡️")
    
    # Sidebar for configuration
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # Asset Management
        st.subheader("🎯 Asset Management")
        
        assets = load_assets()
        
        with st.expander("📝 Edit Assets", expanded=False):
            st.markdown("**Current Assets:**")
            
            # Display and allow deletion
            for i, asset in enumerate(assets):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text(f"{asset.get('software', 'N/A')} {asset.get('version', '')}")
                with col2:
                    if st.button("🗑️", key=f"del_{i}"):
                        assets.pop(i)
                        save_assets(assets)
                        st.rerun()
            
            st.divider()
            st.markdown("**Add New Asset:**")
            
            new_name = st.text_input("Name", placeholder="Web Server", key="new_asset_name")
            new_software = st.text_input("Software", placeholder="PHP", key="new_asset_software")
            new_version = st.text_input("Version", placeholder="8.1", key="new_asset_version")
            
            if st.button("➕ Add Asset"):
                if new_software:
                    new_asset = {
                        "name": new_name or "Asset",
                        "software": new_software,
                        "version": new_version
                    }
                    assets.append(new_asset)
                    if save_assets(assets):
                        st.success("Asset added!")
                        st.rerun()
                else:
                    st.warning("Software name is required")
        
        st.divider()
        
        # Geo/Campaign Filters
        st.subheader("🌍 Focus Areas")
        
        country_filter = st.text_input(
            "Country/Region",
            placeholder="e.g., Mongolia, China, Russia",
            help="Filter threats mentioning specific countries"
        )
        
        campaign_filter = st.text_input(
            "Campaign/Actor",
            placeholder="e.g., APT28, Lazarus",
            help="Filter threats by campaign or threat actor"
        )
        
        keyword_filter = st.text_input(
            "Keywords",
            placeholder="e.g., ransomware, phishing",
            help="Filter threats containing specific keywords"
        )
        
        st.divider()
        
        # Display settings
        st.subheader("📊 Display")
        show_low_severity = st.checkbox("Show Low Severity", value=False)
        max_threats = st.slider("Max Threats to Display", 10, 100, 50)
    
    # Header
    st.title("🛡️ MCP CTI Dashboard")
    st.markdown("**Real-time Cyber Threat Intelligence** | Powered by AlienVault OTX")
    
    # Fetch data
    with st.spinner("Fetching live threat intelligence..."):
        threats = fetch_threats(API_URL)
        stats = fetch_stats(STATS_URL)

    if not threats:
        st.warning("⚠️ No threats found. Check your OTX API key or asset configuration.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(threats)
    df["score"] = pd.to_numeric(df["score"], errors='coerce').fillna(0)
    
    # Apply custom filters
    filtered_df = df.copy()
    
    # Country/Region filter
    if country_filter:
        countries = [c.strip().lower() for c in country_filter.split(",")]
        mask = filtered_df.apply(
            lambda row: any(
                country in str(row["threat_name"]).lower() or 
                country in str(row["value"]).lower() or
                any(country in str(tag).lower() for tag in (row.get("tags", []) or []))
                for country in countries
            ),
            axis=1
        )
        filtered_df = filtered_df[mask]
    
    # Campaign/Actor filter
    if campaign_filter:
        campaigns = [c.strip().lower() for c in campaign_filter.split(",")]
        mask = filtered_df.apply(
            lambda row: any(
                campaign in str(row["threat_name"]).lower() or
                any(campaign in str(tag).lower() for tag in (row.get("tags", []) or []))
                for campaign in campaigns
            ),
            axis=1
        )
        filtered_df = filtered_df[mask]
    
    # Keyword filter
    if keyword_filter:
        keywords = [k.strip().lower() for k in keyword_filter.split(",")]
        mask = filtered_df.apply(
            lambda row: any(
                keyword in str(row["threat_name"]).lower() or
                keyword in str(row["value"]).lower() or
                any(keyword in str(tag).lower() for tag in (row.get("tags", []) or []))
                for keyword in keywords
            ),
            axis=1
        )
        filtered_df = filtered_df[mask]
    
    # Severity filter
    if not show_low_severity:
        filtered_df = filtered_df[filtered_df["severity"] != "Low"]
    
    # Limit results
    filtered_df = filtered_df.head(max_threats)
    
    # Show filter info
    if len(filtered_df) < len(df):
        st.info(f"🔍 Showing {len(filtered_df)} of {len(df)} threats (filtered)")
    
    # --- TOP METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Total Threats",
            len(filtered_df),
            delta=f"{len(df)} total" if len(filtered_df) < len(df) else None,
            help="Total number of threats matching your filters"
        )
    
    with col2:
        avg_score = filtered_df["score"].mean() if len(filtered_df) > 0 else 0
        st.metric(
            "📊 Avg Risk Score",
            f"{avg_score:.1f}/10",
            delta=None,
            help="Average risk score across filtered threats"
        )
    
    with col3:
        critical_count = len(filtered_df[filtered_df["severity"] == "Critical"])
        st.metric(
            "🚨 Critical",
            critical_count,
            delta=None,
            help="Number of critical severity threats"
        )
    
    with col4:
        high_count = len(filtered_df[filtered_df["severity"] == "High"])
        st.metric(
            "⚠️ High",
            high_count,
            delta=None,
            help="Number of high severity threats"
        )
    
    st.divider()
    
    # --- MAIN CHARTS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Severity Distribution")
        severity_counts = filtered_df["severity"].value_counts().reset_index()
        severity_counts.columns = ["Severity", "Count"]
        
        color_map = {
            "Critical": "#dc2626",
            "High": "#ea580c",
            "Medium": "#f59e0b",
            "Low": "#10b981"
        }
        
        fig1 = px.bar(
            severity_counts,
            x="Severity",
            y="Count",
            color="Severity",
            color_discrete_map=color_map,
            text="Count"
        )
        fig1.update_traces(textposition='outside')
        fig1.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Threat Types")
        type_counts = filtered_df["type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        
        fig2 = px.pie(
            type_counts,
            values="Count",
            names="Type",
            hole=0.4
        )
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # --- ADVANCED VISUALIZATIONS ---
    tab1, tab2, tab3 = st.tabs(["📊 Score Analysis", "🏷️ Tag Intelligence", "📅 Timeline"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Score Distribution")
            score_fig = create_score_distribution(filtered_df)
            st.plotly_chart(score_fig, use_container_width=True)
        
        with col2:
            st.markdown("#### References vs Score")
            ref_fig = create_reference_vs_score(filtered_df)
            if ref_fig:
                st.plotly_chart(ref_fig, use_container_width=True)
            else:
                st.info("Reference data not available")
    
    with tab2:
        tag_fig = create_tag_cloud_chart(filtered_df)
        if tag_fig:
            st.plotly_chart(tag_fig, use_container_width=True)
            
            # Show tag insights
            st.markdown("#### 🔍 Tag Insights")
            all_tags = []
            for tags in filtered_df["tags"]:
                if isinstance(tags, list):
                    all_tags.extend(tags)
            
            if all_tags:
                tag_counts = Counter(all_tags)
                top_3 = tag_counts.most_common(3)
                
                cols = st.columns(3)
                for i, (tag, count) in enumerate(top_3):
                    with cols[i]:
                        st.metric(f"#{i+1} Tag", tag, f"{count} threats")
        else:
            st.info("No tag data available")
    
    with tab3:
        timeline_fig = create_timeline_chart(filtered_df)
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)
            
            # Recent threats
            st.markdown("#### 🕐 Recent Threats")
            df_recent = filtered_df.copy()
            df_recent["created"] = pd.to_datetime(df_recent["created"], errors='coerce')
            df_recent = df_recent.dropna(subset=["created"])
            df_recent = df_recent.sort_values("created", ascending=False).head(5)
            
            for _, row in df_recent.iterrows():
                severity_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
                st.markdown(f"{severity_emoji.get(row['severity'], '⚪')} **{row['threat_name'][:80]}** - {row['created'].strftime('%Y-%m-%d')}")
        else:
            st.info("Timeline data not available")
    
    st.divider()
    
    # --- DETAILED THREAT TABLE ---
    st.subheader("📋 Detailed Threat Feed")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=filtered_df["severity"].unique(),
            default=filtered_df["severity"].unique()
        )
    
    with col2:
        type_filter = st.multiselect(
            "Filter by Type",
            options=filtered_df["type"].unique(),
            default=filtered_df["type"].unique()
        )
    
    with col3:
        min_score = st.slider("Minimum Risk Score", 0.0, 10.0, 0.0, 0.5)
    
    # Apply filters
    table_df = filtered_df[
        (filtered_df["severity"].isin(severity_filter)) &
        (filtered_df["type"].isin(type_filter)) &
        (filtered_df["score"] >= min_score)
    ]
    
    st.markdown(f"**Showing {len(table_df)} threats**")
    
    # Display table
    # Only include columns that exist
    available_cols = ["severity", "score", "threat_name", "type", "value"]
    if "tags" in table_df.columns:
        available_cols.append("tags")
    if "created" in table_df.columns:
        available_cols.append("created")
    if "references" in table_df.columns:
        available_cols.append("references")
    
    display_df = table_df[available_cols].copy()
    
    column_config = {
        "score": st.column_config.ProgressColumn(
            "Risk Score",
            help="The risk score of the threat (0-10)",
            format="%.1f",
            min_value=0,
            max_value=10,
        ),
        "severity": st.column_config.TextColumn("Severity"),
        "threat_name": st.column_config.TextColumn("Threat Name", width="large"),
        "type": st.column_config.TextColumn("Type"),
        "value": st.column_config.TextColumn("Indicator", width="medium"),
    }
    
    if "tags" in available_cols:
        column_config["tags"] = st.column_config.ListColumn("Tags")
    if "created" in available_cols:
        column_config["created"] = st.column_config.TextColumn("Date")
    if "references" in available_cols:
        column_config["references"] = st.column_config.NumberColumn("Refs", help="Community references")
    
    st.dataframe(
        display_df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # --- EXPORT ---
    st.divider()
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### 💾 Export Data")
    
    with col2:
        csv = table_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"threats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
