import streamlit as st
import os
import subprocess
from scraper import (
    fetch_html,
    save_raw_data, 
    format_data,
    save_formatted_data,
    calculate_price,
    html_to_markdown_with_readability,
    create_dynamic_listing_model, 
    create_listings_container_model
)
from streamlit_tags import st_tags
import pandas as pd
import json
from datetime import datetime
from assets import PRICING

# Install Playwright browsers on first run
if not os.path.exists("/home/appuser/.cache/ms-playwright"):
    subprocess.run(["playwright", "install", "chromium"], check=True)

st.set_page_config(
    page_title="Web Scraper",
    page_icon="logo.svg",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f0ff 0%, #e6e0ff 100%);
        color: #4a4a4a;
    }
    
    .stTextInput > label,
    .stSelectbox > label {
        color: #2c2c2c !important;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #9370DB;
        border-radius: 4px;
        background-color: white;
        color: #2c2c2c;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #9370DB;
        border-radius: 4px;
        background-color: white;
        color: #2c2c2c;
    }
    
    .main > div {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    h1 {
        color: #6b4e94;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    h3 {
        color: #6b4e94;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        background-color: #9370DB;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 27px;
    }
    
    .stButton>button:hover {
        background-color: #7B68EE;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Custom styling for the tags input */
    .stTags input {
        color: #6b4e94 !important;
    }
    
    /* Styling for tags input field placeholder */
    .stTags input::placeholder {
        color: white !important;  /* Changed to white */
        opacity: 0.7;
    }
    
    /* Styling for the label text */
    .stTags label {
        color: #6b4e94 !important;
    }
    
    /* Styling for the helper text */
    .stTags .st-emotion-cache-1y4p8pa {
        color: #9370DB !important;
    }
    
    /* Navbar styling */
    .stApp header {
        background-color: rgba(147, 112, 219, 0.1);
    }
    
    /* Top navbar text color */
    .stApp header .streamlit-header {
        color: #6b4e94 !important;
    }
    
    /* Tags input field styling */
    .stTags {
        background-color: white !important;
        border: 2px solid #9370DB !important;
        border-radius: 4px !important;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 20px;
        left: 0;
        right: 0;
        padding: 20px;
        text-align: center;
        color: #6b4e94;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.svg", width=100)
with col2:
    st.markdown("<h1 style='text-align: left;'>Universal Web Scraper</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b4e94; font-size: 1.2em;'>Scrape data beautifully</p>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("### 🔮 Configuration")
    url_input = st.text_input("Enter URL", placeholder="https://example.com")
    model_selection = st.selectbox("Select Model", options=list(PRICING.keys()), index=0)
    
    st.markdown("### 🏷️ Fields to Extract")
    tags = st_tags(
        label='Add fields to extract (press enter after each)',
        text='Press enter to add a field',
        value=[],
        suggestions=[],
        maxtags=-1,
        key='tags_input'
    )
    st.caption("Enter each field you want to extract and press enter")

with right_col:
    st.markdown("### 📊 Results")
    
    if st.button("Start Scraping"):
        with st.spinner('🌟 Magic in progress...'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            try:
                raw_html = fetch_html(url_input)
                markdown = html_to_markdown_with_readability(raw_html)
                save_raw_data(markdown, timestamp)
                
                DynamicListingModel = create_dynamic_listing_model(tags)
                DynamicListingsContainer = create_listings_container_model(DynamicListingModel)
                
                formatted_data, tokens_count = format_data(markdown, DynamicListingsContainer, DynamicListingModel, model_selection)
                input_tokens, output_tokens, total_cost = calculate_price(tokens_count, model=model_selection)
                
                df = save_formatted_data(formatted_data, timestamp)
                
                st.success("✨ Scraping completed successfully!")
                st.dataframe(df, use_container_width=True)
                
                with st.expander("💫 Token Usage Details"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Input Tokens", input_tokens)
                    col2.metric("Output Tokens", output_tokens)
                    col3.metric("Total Cost", f"${total_cost:.4f}")
                
                st.markdown("### 📥 Download Results")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "📋 JSON",
                        data=json.dumps(formatted_data.dict() if hasattr(formatted_data, 'dict') else formatted_data, indent=4),
                        file_name=f"{timestamp}_data.json"
                    )
                with col2:
                    st.download_button(
                        "📊 CSV",
                        data=df.to_csv(index=False),
                        file_name=f"{timestamp}_data.csv"
                    )
                with col3:
                    st.download_button(
                        "📝 Markdown",
                        data=markdown,
                        file_name=f"{timestamp}_data.md"
                    )
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

st.markdown(
    "<div class='footer'>"
    "Made by Priyankesh, <a href='https://github.com/priyankeshh' style='color: #9370DB;'>Github</a>"
    "</div>", 
    unsafe_allow_html=True
)