import streamlit as st
from google import genai
import datetime

# 1. Page & HUD Setup
st.set_page_config(page_title="FRIDAY v1.5 Vocal", page_icon="🔊")

st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: #00d4ff; }
    .stChatMessage { border-radius: 15px; border-left: 3px solid #00d4ff; background: rgba(0, 212, 255, 0.05); }
    </style>
""", unsafe_allow_html=True)

# --- JAVASCRIPT FOR VOICE OUTPUT ---
def speak_text(text):
    # This script triggers the phone's native TTS
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance();
    msg.text = "{text.replace('"', '')}";
    msg.rate = 1.1; 
    msg.pitch = 1.2;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

st.title("F.R.I.D.A.Y. Vocal Interface")

# 2. Date & Time Data
now = datetime.datetime.now()
current_time = now.strftime("%I:%M %p")
current_date = now.strftime("%B %d, %Y")

# 3. AI Logic Setup
if "GEMINI_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Voice Input (Microphone)
audio_input = st.audio_input("Speak to FRIDAY")

# 5. Logical Processing
prompt = st.chat_input("Directives, Boss?")

if audio_input:
    # Note: Transcription would happen here; for now we use a status trigger
    prompt = "Friday, give me a verbal status report."

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction=f"You are FRIDAY. Today is {current_date}, {current_time}. Be witty, brief (keep responses under 3 sentences for better speech), and call the user Boss.",
                tools=[{"google_search": {}}],
                temperature=0.4
            ),
            contents=[m["content"] for m in st.session_state.messages]
        )
        
        output_text = response.text
        st.markdown(output_text)
        
        # TRIGGER THE VOICE
        speak_text(output_text)
        
        st.session_state.messages.append({"role": "assistant", "content": output_text})
