import os
import requests
import json
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

API_URL = os.getenv("MCP_API_URL", "http://localhost:9000/threats")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def fetch_threats(url: str):
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch threats: {e}")
        return []


def simple_summary(threats):
    # Minimal, local summarizer for demo purposes
    if not threats:
        return "No relevant threats found."
    names = [t.get("threat_name") or t.get("value") for t in threats]
    unique = list(dict.fromkeys(names))
    return f"Found {len(threats)} relevant indicators across {len(unique)} distinct threat names. Top examples: {', '.join(unique[:5])}"


def main():
    st.title("MCP CTI Dashboard - Minimal Demo")
    st.markdown("Displays threats filtered against local asset inventory via the MCP server.")

    threats = fetch_threats(API_URL)

    if threats:
        st.subheader("Relevant Threats")
        st.table(threats)

        if ANTHROPIC_API_KEY:
            st.info("Anthropic key found — optional LLM summarization available.")
            if st.button("Generate LLM Summary"):
                try:
                    # Try to use anthropic package if installed
                    from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

                    client = Anthropic(api_key=ANTHROPIC_API_KEY)
                    prompt = HUMAN_PROMPT + "Summarize these threats in 3 bullets:\n" + json.dumps(threats) + AI_PROMPT
                    resp = client.completions.create(model="claude-2", prompt=prompt, max_tokens_to_sample=200)
                    summary = resp.get("completion") or resp.get("completion_text") or str(resp)
                except Exception:
                    summary = simple_summary(threats)
                st.subheader("LLM Summary")
                st.write(summary)
        else:
            st.subheader("Summary")
            st.write(simple_summary(threats))
    else:
        st.write("No threats to display.")


if __name__ == "__main__":
    main()
