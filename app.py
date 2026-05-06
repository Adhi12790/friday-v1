import streamlit as st
from google import genai
import datetime
import pytz

# 1. CORE CONFIGURATION
st.set_page_config(page_title="FRIDAY v1.6", page_icon="🤖", layout="wide")

# Indian Standard Time Setup
ist = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(ist)
current_time = now.strftime("%I:%M %p")
current_date = now.strftime("%B %d, %Y")

# 2. WHATSAPP-STYLE HUD & FLOATING INPUT
st.markdown(f"""
    <style>
    /* Dark Stark Theme */
    .stApp {{ background-color: #050a14; color: #00d4ff; }}
    
    /* WhatsApp-style floating input container */
    div[data-testid="stChatInput"] {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 85%;
        z-index: 1000;
    }}

    /* Custom Chat Bubbles */
    .stChatMessage {{ 
        border-radius: 20px; 
        border: 1px solid #00d4ff22; 
        background: rgba(0, 212, 255, 0.03);
        margin-bottom: 15px;
    }}
    
    /* Hide the 'Stop' button on audio to make it cleaner */
    button[title="Stop recording"] {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# 3. BRAIN SETUP (Gemini 2.5)
if "GEMINI_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("System Error: API Key missing.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. JAVASCRIPT VOCALIZER
def speak(text):
    clean_text = text.replace('"', '').replace("'", "")
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{clean_text}");
    msg.rate = 1.1; msg.pitch = 1.1;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0)

# 5. UI HEADER
st.title("F.R.I.D.A.Y.")
st.caption(f"System Time: {current_time} | Status: Nominal")

# 6. DISPLAY CONVERSATION
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. MULTI-MODAL INPUT (Voice & Text)
# Floating audio input at the top for accessibility
audio_data = st.audio_input("Vocal Override")

# Chat input will float at the bottom-right due to CSS
prompt = st.chat_input("Directives, Boss?")

# Logic for input
if audio_data:
    prompt = "Friday, perform a vocal diagnostics and status report."

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction=f"You are FRIDAY. Today is {current_date}, {current_time} in Kerala. Be witty, efficient, and call the user Boss. Keep verbal answers under 3 sentences.",
                tools=[{"google_search": {}}],
                temperature=0.3
            ),
            contents=[m["content"] for m in st.session_state.messages]
        )
        
        res_text = response.text
        st.markdown(res_text)
        speak(res_text) # Verbalize
        st.session_state.messages.append({"role": "assistant", "content": res_text})
