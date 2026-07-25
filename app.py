import streamlit as st
import re
import math
import time

# ==========================================
# 🧠 ADVANCED LOCAL NLP ENGINE (AIML CORE)
# ==========================================
class AdvancedNLPEngine:
    def __init__(self):
        # Weighted Vocabulary Dictionary (TF-IDF Simulation)
        self.urgency_weights = {
            'urgent': 0.85, 'immediately': 0.80, 'action required': 0.90,
            'suspended': 0.85, 'locked': 0.85, 'block': 0.75, 'expire': 0.70,
            'alert': 0.60, 'warning': 0.65, 'permanent closure': 0.95
        }
        
        self.financial_weights = {
            'bank': 0.60, 'account': 0.50, 'pan': 0.85, 'kyc': 0.90, 'aadhar': 0.85,
            'debit card': 0.80, 'credit card': 0.80, 'sbi': 0.50, 'hdfc': 0.50, 'icici': 0.50,
            'lottery': 0.95, 'winner': 0.90, 'cash prize': 0.90, '$/day': 0.85, 'rs': 0.40
        }
        
        self.action_weights = {
            'click here': 0.90, 'verify': 0.75, 'update': 0.70, 'login': 0.75,
            'link': 0.60, 'otp': 0.85, 'password': 0.80, 'pin': 0.80, 'claim': 0.85
        }

    def tokenize_and_clean(self, text):
        # Convert to lowercase and remove special characters for base tokenization
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return text, tokens

    def detect_suspicious_patterns(self, text):
        patterns = {
            'hidden_links': r'\[.*?\]\(http.*?\)',
            'raw_urls': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'obfuscation': r'[a-z0-9]+@[a-z0-9]+\.[a-z]+', # Emails hiding in text
            'phone_numbers': r'\+?\d{10,12}'
        }
        
        detected = []
        for name, pattern in patterns.items():
            if re.search(pattern, text):
                detected.append(name)
        return detected

    def analyze(self, raw_text):
        if not raw_text.strip():
            return None
            
        text_lower, tokens = self.tokenize_and_clean(raw_text)
        
        # 1. Feature Extraction & Scoring
        urgency_score = 0
        financial_score = 0
        action_score = 0
        matched_flags = []
        
        # Scan for Urgency
        for word, weight in self.urgency_weights.items():
            if word in text_lower:
                urgency_score += weight
                matched_flags.append(word)
                
        # Scan for Financial Data
        for word, weight in self.financial_weights.items():
            if word in text_lower:
                financial_score += weight
                matched_flags.append(word)
                
        # Scan for Action Hooks
        for word, weight in self.action_weights.items():
            if word in text_lower:
                action_score += weight
                matched_flags.append(word)

        # 2. Pattern Matching for Malicious Links
        patterns = self.detect_suspicious_patterns(raw_text)
        pattern_penalty = len(patterns) * 1.5
        
        # 3. Calculate Non-Linear Threat Probability (Sigmoid-like activation)
        total_threat_score = urgency_score + financial_score + action_score + pattern_penalty
        
        # Normalize score to 0-100 range mathematically
        raw_spam_pct = (1 - math.exp(-total_threat_score / 2.5)) * 100
        
        # Heuristic Overrides for severe combinations
        if 'kyc' in text_lower and 'link' in text_lower:
            raw_spam_pct = max(raw_spam_pct, 92.0)
        if 'locked' in text_lower and 'verify' in text_lower:
            raw_spam_pct = max(raw_spam_pct, 88.0)
            
        final_spam_pct = min(int(raw_spam_pct), 99)
        final_safe_pct = 100 - final_spam_pct
        
        # 4. Generate Dynamic Explanations
        if final_spam_pct > 75:
            reason_en = f"CRITICAL MATCH: NLP detected a severe phishing sequence. Found {len(matched_flags)} high-risk vectors (e.g., '{matched_flags[0] if matched_flags else 'link'}', '{matched_flags[1] if len(matched_flags)>1 else 'update'}')."
            alert_en = "🚨 CRITICAL THREAT DETECTED"
            reason_te = f"అధిక ముప్పు! ఈ సందేశంలో మోసపూరిత పదాలు ({matched_flags[0] if matched_flags else 'లింక్'}) గుర్తించబడ్డాయి. ఇది ఫిషింగ్ దాడి కావచ్చు."
            alert_te = "🚨 క్లిష్టమైన ముప్పు కనుగొనబడింది"
            reason_hi = f"उच्च खतरा! प्राकृतिक भाषा प्रसंस्करण ने धोखाधड़ी वाले शब्दों की पहचान की है।"
            alert_hi = "🚨 गंभीर खतरा पाया गया"
        elif final_spam_pct > 40:
            reason_en = "MODERATE MATCH: The text contains promotional language or suspicious requests. Exercise caution."
            alert_en = "⚠️ PROMOTIONAL / SUSPICIOUS"
            reason_te = "ఈ సందేశం ఒక ప్రకటన లేదా అనుమానాస్పద అభ్యర్థనలా కనిపిస్తోంది. జాగ్రత్త వహించండి."
            alert_te = "⚠️ ప్రమోషనల్ కంటెంట్"
            reason_hi = "यह एक विज्ञापन या संदिग्ध संदेश जैसा लगता है। सावधानी बरतें।"
            alert_hi = "⚠️ प्रचार सामग्री"
        else:
            reason_en = "SECURE: No malicious intent, financial hooks, or urgency parameters detected in the lexical analysis."
            alert_en = "✅ CONTENT IS SECURE"
            reason_te = "ఈ సందేశం సాధారణంగా ఉంది. ఇందులో ఎలాంటి ప్రమాదకరమైన లింకులు లేదా ఆర్థిక అభ్యర్థనలు లేవు."
            alert_te = "✅ కంటెంట్ సురక్షితమైనది"
            reason_hi = "यह संदेश सामान्य और सुरक्षित है। कोई दुर्भावनापूर्ण इरादा नहीं पाया गया।"
            alert_hi = "✅ सामग्री सुरक्षित है"

        return {
            "safe_percentage": final_safe_pct,
            "spam_percentage": final_spam_pct,
            "reason_en": reason_en,
            "alert_en": alert_en,
            "reason_te": reason_te,
            "alert_te": alert_te,
            "reason_hi": reason_hi,
            "alert_hi": alert_hi,
            "matched_keywords": matched_flags
        }

# ==========================================
# 🖥️ STREAMLIT USER INTERFACE
# ==========================================
st.set_page_config(page_title="Spam Destruction System", page_icon="🕵️‍♂️", layout="centered")

# Initialize Session State
if 'show_report' not in st.session_state:
    st.session_state.show_report = False
    st.session_state.ai_data = None

# Custom CSS styling
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; color: #333333; }
    h1, h2, h3 { color: #1A5276 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stTextArea textarea { background-color: #FFFFFF; color: #333333; border: 1px solid #BDC3C7; border-radius: 8px; }
    .stButton>button { background-color: #2980B9; color: #FFFFFF; border: none; border-radius: 8px; padding: 12px 24px; font-weight: bold; width: 100%; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button:hover { background-color: #1A5276; color: white; transform: translateY(-2px); }
    .report-box { background-color: #FFFFFF; padding: 25px; border-radius: 12px; border-top: 5px solid #2980B9; margin-top: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.08); }
    .scanner-bar { width: 100%; height: 4px; background-color: #2980B9; border-radius: 5px; margin-top: 10px; margin-bottom: 10px; animation: scan 1.5s infinite ease-in-out; }
    @keyframes scan { 0% { transform: scaleX(0); opacity: 0.5; } 50% { transform: scaleX(1); opacity: 1; } 100% { transform: scaleX(0); opacity: 0.5; } }
    </style>
""", unsafe_allow_html=True)

st.title("🕵️‍♂️ Spam Destruction System")
st.markdown("**Advanced On-Device NLP Threat Detection Engine**")
st.markdown("---")

news_input = st.text_area("Initialize Target Scan (Paste Text):", height=150, placeholder="Enter target data to scan for vulnerabilities...")

if st.button("Execute Hack & Analyze 🚀"):
    if news_input.strip() == "":
        st.warning("⚠️ Warning: Empty string detected. Enter data to scan.")
    else:
        with st.spinner('Initializing On-Device NLP Weights & Analyzing...'):
            st.markdown('<div class="scanner-bar"></div>', unsafe_allow_html=True)
            time.sleep(1.5) # Simulated computational delay
            
            # Call our local AIML Engine!
            engine = AdvancedNLPEngine()
            st.session_state.ai_data = engine.analyze(news_input)
            st.session_state.show_report = True
            st.toast("✅ NLP Processing Complete!", icon="🧠")

# Display Results
if st.session_state.show_report and st.session_state.ai_data:
    ai_data = st.session_state.ai_data
    
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.subheader("📊 Cyber Threat Report")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="✅ Safe Confidence", value=f"{ai_data['safe_percentage']}%")
    with col2:
        st.metric(label="❌ Threat Level", value=f"{ai_data['spam_percentage']}%")
        
    st.progress(ai_data['spam_percentage'] / 100)
    st.markdown("---")
    
    lang = st.radio("Select Language / భాష ఎంచుకోండి / भाषा चुनें:", ["English", "తెలుగు", "हिन्दी"], horizontal=True)
    
    if lang == "తెలుగు":
        reason_text = ai_data['reason_te']
        alert_text = ai_data['alert_te']
    elif lang == "हिन्दी":
        reason_text = ai_data['reason_hi']
        alert_text = ai_data['alert_hi']
    else:
        reason_text = ai_data['reason_en']
        alert_text = ai_data['alert_en']
    
    st.markdown("### 📝 Core NLP Scan Summary")
    st.info(f"**Explanation:**\n\n{reason_text}")
    
    if ai_data['matched_keywords']:
        st.markdown(f"**🔴 Detected Threat Vectors:** `{', '.join(ai_data['matched_keywords'][:5])}`")
    
    spam_val = ai_data['spam_percentage']
    if spam_val > 80:
        st.error(alert_text)
    elif spam_val > 40:
        st.warning(alert_text)
    else:
        st.success(alert_text)
        
    st.markdown('</div>', unsafe_allow_html=True)
