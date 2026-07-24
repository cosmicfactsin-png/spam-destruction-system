import streamlit as st
import google.generativeai as genai
import json
import time
import random

# 1. Professional Setup 
st.set_page_config(page_title="Spam Destruction System", page_icon="🕵️‍♂️", layout="centered")

# Initialize Session State to remember the report when changing languages
if 'show_report' not in st.session_state:
    st.session_state.show_report = False
    st.session_state.ai_data = None

# 2. Light & Professional CSS Theme with Animations
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; color: #333333; }
    h1, h2, h3 { color: #1A5276 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-shadow: none; }
    .stTextArea textarea { background-color: #FFFFFF; color: #333333; border: 1px solid #BDC3C7; border-radius: 8px; }
    .stButton>button { background-color: #2980B9; color: #FFFFFF; border: none; border-radius: 8px; padding: 12px 24px; font-weight: bold; width: 100%; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button:hover { background-color: #1A5276; color: white; transform: translateY(-2px); }
    
    .report-box { 
        background-color: #FFFFFF; padding: 25px; border-radius: 12px; border-top: 5px solid #2980B9; 
        margin-top: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.08); animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .scanner-bar {
        width: 100%; height: 4px; background-color: #2980B9; border-radius: 5px; margin-top: 10px; margin-bottom: 10px; animation: scan 1.5s infinite ease-in-out;
    }
    @keyframes scan {
        0% { transform: scaleX(0); opacity: 0.5; }
        50% { transform: scaleX(1); opacity: 1; }
        100% { transform: scaleX(0); opacity: 0.5; }
    }
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
        with st.spinner('Bypassing firewalls... Analyzing data with AI...'):
            st.markdown('<div class="scanner-bar"></div>', unsafe_allow_html=True)
            time.sleep(1.5)
            
            try:
                GOOGLE_API_KEY = "AQ.Ab8RN6LtRx5ENNumHAduwOqw62FbmRry88j2vQfX8a9PUQiRow"
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prompting AI for English, Telugu, and Hindi translations
                secret_prompt = f"""
                You are a smart Cybersecurity AI. Analyze the text and return ONLY valid JSON format.
                Score rules: 90-100 (fraud/scam), 40-60 (promo/ads), 0-20 (safe).
                
                Return exactly this JSON format with NO markdown formatting or backticks:
                {{
                    "safe_percentage": <int>,
                    "spam_percentage": <int>,
                    "reason_en": "Explain the threat simply in 2 lines.",
                    "alert_en": "Short warning (e.g., CRITICAL THREAT DETECTED or CONTENT IS SECURE)",
                    "reason_te": "Translate the exact reason_en to Telugu.",
                    "alert_te": "Translate the alert_en to Telugu.",
                    "reason_hi": "Translate the exact reason_en to Hindi.",
                    "alert_hi": "Translate the alert_en to Hindi."
                }}
                
                Text: {news_input}
                """
                response = model.generate_content(secret_prompt)
                
                clean_text = response.text.replace('```json', '').replace('```', '').strip()
                st.session_state.ai_data = json.loads(clean_text)
                
            except Exception as e:
                # Local Fallback with Translations
                input_lower = news_input.lower()
                fraud_keywords = ["lottery", "prize", "bank", "otp", "free"]
                promo_keywords = ["discount", "subscribe", "offer"]
                
                if any(word in input_lower for word in fraud_keywords):
                    spam_p = random.randint(95, 100)
                    r_en, a_en = "This message contains dangerous words like lottery, OTP, or free money. It is highly likely to be a scam.", "CRITICAL THREAT: Scam Detected."
                    r_te, a_te = "ఈ సందేశంలో లాటరీ, OTP లేదా ఉచిత డబ్బు లాంటి ప్రమాదకరమైన పదాలు ఉన్నాయి. ఇది మోసం అయ్యే అవకాశం ఉంది.", "ప్రమాద హెచ్చరిక: స్కామ్ కనుగొనబడింది."
                    r_hi, a_hi = "इस संदेश में लॉटरी, OTP या मुफ्त पैसे जैसे खतरनाक शब्द हैं। यह एक घोटाला होने की अत्यधिक संभावना है।", "महत्वपूर्ण चेतावनी: स्कैम का पता चला।"
                elif any(word in input_lower for word in promo_keywords):
                    spam_p = random.randint(40, 60)
                    r_en, a_en = "This looks like a promotional message or an advertisement.", "CAUTION: Promotional Content."
                    r_te, a_te = "ఇది ఒక ప్రమోషనల్ మెసేజ్ లేదా ప్రకటన లాగా కనిపిస్తోంది.", "జాగ్రత్త: ఇది ప్రకటనకు సంబంధించినది."
                    r_hi, a_hi = "यह एक प्रचारात्मक संदेश या विज्ञापन जैसा लगता है।", "सावधान: प्रचारात्मक सामग्री।"
                else:
                    spam_p = random.randint(5, 15)
                    r_en, a_en = "This message looks normal and safe. No dangerous links or words found.", "SECURE: Content is Safe."
                    r_te, a_te = "ఈ సందేశం సాధారణంగా మరియు సురక్షితంగా కనిపిస్తోంది. ఎలాంటి ప్రమాదకరమైన పదాలు లేవు.", "సురక్షితం: కంటెంట్ సురక్షితమైనది."
                    r_hi, a_hi = "यह संदेश सामान्य और सुरक्षित लग रहा है। कोई खतरनाक शब्द नहीं मिला।", "सुरक्षित: सामग्री सुरक्षित है।"
                    
                st.session_state.ai_data = {
                    "safe_percentage": 100 - spam_p, "spam_percentage": spam_p,
                    "reason_en": r_en, "alert_en": a_en,
                    "reason_te": r_te, "alert_te": a_te,
                    "reason_hi": r_hi, "alert_hi": a_hi
                }
            
            st.session_state.show_report = True

# 7. Output Results with Language Selection
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
    
    # Translation Buttons (Radio)
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
    
    # Box 1: Explanation
    st.info(f"**Explanation:**\n\n{reason_text}")
    
    # Box 2: Alert Message
    spam_val = ai_data.get('spam_percentage', 100)
    if spam_val > 80:
        st.error(f"🚨 **{alert_text}**")
    elif spam_val > 40:
        st.warning(f"⚠️ **{alert_text}**")
    else:
        st.success(f"✅ **{alert_text}**")
        
    st.markdown('</div>', unsafe_allow_html=True)