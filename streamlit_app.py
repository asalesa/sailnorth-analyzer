import streamlit as st
from main import get_site_text, analyze_company
import json

st.set_page_config(page_title="SailNorth ICP Analyzer", layout="wide")
st.title("🚢 SailNorth ICP Analyzer")

st.markdown("Paste a maritime company website below to analyze it for vessel ownership, crewing scale, and ICP fit.")

url = st.text_input("Enter company website (e.g. https://www.schultegroup.com)")

if st.button("Analyze"):
    with st.spinner("Scraping website and analyzing..."):
        try:
            site_text = get_site_text(url)
            result = analyze_company(url, site_text)
            parsed = json.loads(result)
            st.success("✅ Analysis Complete!")
            st.subheader("Summary")
            st.markdown(parsed.get("Company summary", ""))
            st.subheader("Why this company fits (or not) the ICP")
            st.markdown(parsed.get("Why they fit (or not) SailNorth’s ICP", ""))

            st.subheader("Structured Output")
            st.json(parsed)
        except Exception as e:
            st.error(f"Something went wrong: {e}")