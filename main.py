import requests
from bs4 import BeautifulSoup
import tldextract
import openai
import streamlit as st  # 👈 this is important

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_site_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ')
        return ' '.join(text.split())
    except Exception as e:
        return f"Error loading site: {e}"

def analyze_company(website, site_text):
    prompt = f"""
You are an expert maritime analyst helping a SaaS startup called SailNorth.

Based on the following company website content, extract structured info. Only use what's stated or strongly implied.

Website: {website}

Content: {site_text[:8000]}

Return a JSON with these fields:
- Owns vessels? (yes/no/unknown)
- Number of vessels owned (number or range)
- Manages vessels? (yes/no/unknown)
- Number of vessels managed (number or range)
- Countries of operation
- Headquarters
- Estimated number of seafarers
- Fleet types (e.g., tankers, bulk, ro-ro)
- Specific vessels (if listed)
- Fleet page URL (if any)
- Key contacts (roles only, e.g., Crewing Director)
- Company summary (2–4 sentences)
- Why they fit (or not) SailNorth’s ICP
- Confidence per field: high / medium / low

Respond only in raw JSON.
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content