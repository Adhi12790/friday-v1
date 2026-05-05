import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="FRIDAY v2.5 Pro", page_icon="⚡")

# Force a full-screen mobile experience
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">', unsafe_allow_html=True)
st.markdown('<meta name="mobile-web-app-capable" content="yes">', unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: #00d4ff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00d4ff22; }
    </style>
    """, unsafe_allow_html=True)

st.title("FRIDAY: v2.5 Pro Online")

# Setup the New 2026 Client
if "GEMINI_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Missing API Key in Streamlit Secrets.")
    st.stop()

# Initialize Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if prompt := st.chat_input("Directives, Boss?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # FRIDAY Response using Gemini 2.5 Flash
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction="You are FRIDAY. You are a high-level AI assistant. Be witty, direct, and call the user 'Boss'.",
                temperature=0.7
            ),
            contents=prompt
        )
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
