import streamlit as st
import requests
import urllib.parse
import json
import time

# 1. Professional Setup 
st.set_page_config(page_title="Spam Destruction System", page_icon="🕵️‍♂️", layout="centered")

if 'show_report' not in st.session_state:
    st.session_state.show_report = False
    st.session_state.ai_data = None

# 2. Light & Professional CSS Theme
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; color: #333333; }
    h1, h2, h3 { color: #1A5276 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-shadow: none; }
    .stTextArea textarea { background-color: #FFFFFF; color: #333333; border: 1px solid #BDC3C7; border-radius: 8px; }
    .stButton>button { background-color: #2980B9; color: #FFFFFF; border: none; border-radius: 8px; padding: 12px 24px; font-weight: bold; width: 100%; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button:hover { background-color: #1A5276; color: white; transform: translateY(-2px); }
    .report-box { background-color: #FFFFFF; padding: 25px; border-radius: 12px; border-top: 5px solid #2980B9; margin-top: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.08); }
    .scanner-bar { width: 100%; height: 4px; background-color: #2980B9; border-radius: 5px; margin-top: 10px; margin-bottom: 10px; animation: scan 1.5s infinite ease-in-out; }
    @keyframes scan { 0% { transform: scaleX(0); opacity: 0.5; } 50% { transform: scaleX(1); opacity: 1; } 100% { transform: scaleX(0); opacity: 0.5; } }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.title("🕵️‍♂️ Spam Destruction System")
st.markdown("**Advanced Cyber Threat & Phishing Detection Engine**")
st.markdown("---")

# 4. Input Section
news_input = st.text_area("Initialize Target Scan (Paste Text):", height=150, placeholder="Enter target data to scan for vulnerabilities...")

if st.button("Execute Hack & Analyze 🚀"):
    if news_input.strip() == "":
        st.warning("⚠️ Warning: Empty string detected. Enter data to scan.")
    else:
        with st.spinner('Bypassing API Keys... Connecting directly to Open AI Neural Network...'):
            st.markdown('<div class="scanner-bar"></div>', unsafe_allow_html=True)
            time.sleep(1.5)
            
            try:
                # ==========================================
                # ZERO API KEY MAGIC (Using Free Pollinations AI)
                # ==========================================
                secret_prompt = f"""
                You are a smart Cybersecurity AI. Analyze the text for spam/phishing.
                Respond ONLY with a valid JSON object. No explanation, no markdown blocks.
                Score rules: 90-100 (fraud), 40-60 (promo), 0-20 (safe).
                Format exactly like this:
                {{
                    "safe_percentage": 10,
                    "spam_percentage": 90,
                    "reason_en": "Reason in English",
                    "alert_en": "CRITICAL THREAT DETECTED",
                    "reason_te": "తెలుగులో కారణం",
                    "alert_te": "ముప్పు కనుగొనబడింది",
                    "reason_hi": "हिंदी में कारण",
                    "alert_hi": "खतरा"
                }}
                Text to analyze: {news_input}
                """
                
                # Encode text for URL
                encoded_prompt = urllib.parse.quote(secret_prompt)
                url = f"https://text.pollinations.ai/{encoded_prompt}"
                
                response = requests.get(url)
                
                if response.status_code == 200:
                    clean_text = response.text.replace('```json', '').replace('```', '').strip()
                    # Find where JSON actually starts to avoid any extra text
                    start_idx = clean_text.find('{')
                    end_idx = clean_text.rfind('}') + 1
                    json_str = clean_text[start_idx:end_idx]
                    
                    st.session_state.ai_data = json.loads(json_str)
                    st.session_state.show_report = True
                    st.toast("✅ Connected to Free Open AI Network!", icon="🚀")
                else:
                    st.error("❌ **CRITICAL ERROR: AI Server Down!**")
                    st.session_state.show_report = False
                    
            except Exception as e:
                st.error("❌ **CRITICAL ERROR: Scan Failed!**")
                st.warning(f"Error Log: {e}")
                st.session_state.show_report = False

# 7. Output Results
if st.session_state.show_report and st.session_state.ai_data:
    ai_data = st.session_state.ai_data
    
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.subheader("📊 Cyber Threat Report")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="✅ Safe Confidence", value=f"{ai_data.get('safe_percentage', 0)}%")
    with col2:
        st.metric(label="❌ Threat Level", value=f"{ai_data.get('spam_percentage', 100)}%")
        
    st.progress(ai_data.get('spam_percentage', 100) / 100)
    st.markdown("---")
    
    lang = st.radio("Select Language / భాష ఎంచుకోండి / भाषा चुनें:", ["English", "తెలుగు", "हिन्दी"], horizontal=True)
    
    if lang == "తెలుగు":
        reason_text = ai_data.get('reason_te', ai_data.get('reason_en', ''))
        alert_text = ai_data.get('alert_te', ai_data.get('alert_en', ''))
    elif lang == "हिन्दी":
        reason_text = ai_data.get('reason_hi', ai_data.get('reason_en', ''))
        alert_text = ai_data.get('alert_hi', ai_data.get('alert_en', ''))
    else:
        reason_text = ai_data.get('reason_en', '')
        alert_text = ai_data.get('alert_en', '')
    
    st.markdown("### 📝 AI Scan Summary")
    st.info(f"**Explanation:**\n\n{reason_text}")
    
    spam_val = ai_data.get('spam_percentage', 100)
    if spam_val > 80:
        st.error(f"🚨 **{alert_text}**")
    elif spam_val > 40:
        st.warning(f"⚠️ **{alert_text}**")
    else:
        st.success(f"✅ **{alert_text}**")
        
    st.markdown('</div>', unsafe_allow_html=True)
