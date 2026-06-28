import streamlit as st
import google.generativeai as genai
import json

# Setup clear presentation layout
st.set_page_config(page_title="Google Ads RSA Copy Generator", page_icon="📝", layout="wide")

st.title("📝 Google RSA Validator & Permutation Generator")
st.write("Instantly generate copy optimized for Google Ads with built-in real-time character constraints.")

# Sidebar configuration for global variables
st.sidebar.header("Platform Credentials")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Workspace Input Fields
st.subheader("1. Campaign Configuration")
col_1, col_2 = st.columns(2)

with col_1:
    product_name = st.text_input("Product or Business Name", placeholder="e.g., Al Adil Trading")
    product_desc = st.text_area("Core Value Proposition / Key Features", placeholder="e.g., Authentic Indian groceries, organic spices, and traditional sweets delivered fast in the UAE.")

with col_2:
    target_audience = st.text_input("Target Audience Description", value="Expats looking for authentic home flavors")
    cta_focus = st.selectbox("Primary Call to Action (CTA) Focus", ["Shop Now / Buy Online", "Get Offer / Discount", "Learn More / Visit Site"])

def generate_rsa_copy(prod, desc, audience, cta, api):
    genai.configure(api_key=api)
    
    # Instruct the AI to act with absolute structural precision
    prompt = f"""
    You are an elite Google Ads PPC Copywriter. 
    Generate highly optimized copy assets for a Responsive Search Ad (RSA) based on these parameters:
    - Product/Business: {prod}
    - Description: {desc}
    - Audience: {audience}
    - CTA Angle: {cta}
    
    STRICT COMPLIANCE RULES:
    1. You must output EXACTLY 15 headlines. Every single headline MUST be 30 characters or less.
    2. You must output EXACTLY 4 descriptions. Every single description MUST be 90 characters or less.
    3. Rely heavily on direct call-to-actions, keyword inclusion, and explicit benefits.
    
    You must format your response strictly as a clean JSON object. Do not include markdown code blocks around the JSON. Match this structure:
    {{
       "headlines": [
          "Headline 1 max 30 chars",
          "Headline 2 max 30 chars"
       ],
       "descriptions": [
          "Description 1 max 90 chars",
          "Description 2 max 90 chars"
       ]
    }}
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)

# Execution Pipeline
if st.button("Generate & Validate RSA Assets"):
    if not api_key:
        st.error("Please enter your free Gemini API Key in the sidebar.")
    elif not product_name or not product_desc:
        st.error("Please fill in your Product Name and Description fields.")
    else:
        with st.spinner("Writing ad assets and running safety character audits..."):
            try:
                ad_assets = generate_rsa_copy(product_name, product_desc, target_audience, cta_focus, api_key)
                
                st.success("Ad Copy Assets Compiled and Verified Successfully!")
                st.markdown("---")
                
                # Render headlines layout
                st.subheader("🎯 Generated Headlines (Max 30 Characters)")
                st.caption("Review character counts below. Click the top-right copy icon on any code box to grab it instantly for Google Ads Editor.")
                
                h_col1, h_col2, h_col3 = st.columns(3)
                all_headlines = ad_assets.get("headlines", [])
                
                for index, headline in enumerate(all_headlines):
                    char_count = len(headline)
                    # Assign rows cleanly across the 3 visual columns
                    target_col = h_col1 if index < 5 else (h_col2 if index < 10 else h_col3)
                    
                    with target_col:
                        if char_count <= 30:
                            st.success(f"Headline {index+1}: {char_count}/30 Chars")
                        else:
                            st.error(f"Headline {index+1} Exceeded: {char_count}/30 Chars")
                        st.code(headline, language="text")
                
                st.markdown("---")
                
                # Render descriptions layout
                st.subheader("📝 Generated Descriptions (Max 90 Characters)")
                
                d_col1, d_col2 = st.columns(2)
                all_descriptions = ad_assets.get("descriptions", [])
                
                for index, desc in enumerate(all_descriptions):
                    char_count = len(desc)
                    target_col = d_col1 if index < 2 else d_col2
                    
                    with target_col:
                        if char_count <= 90:
                            st.success(f"Description {index+1}: {char_count}/90 Chars")
                        else:
                            st.error(f"Description {index+1} Exceeded: {char_count}/90 Chars")
                        st.code(desc, language="text")
                        
            except Exception as e:
                st.error(f"Execution failed. Please confirm your API key or formatting: {str(e)}")