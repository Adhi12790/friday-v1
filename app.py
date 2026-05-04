import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="FRIDAY v1", page_icon="⚙️")

# Custom CSS for the "Iron Man" look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #5ce1e6; }
    </style>
    """, unsafe_allow_html=True)

st.title("FRIDAY: Online")

# Setup AI with a secure secret key
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key. Please configure it in Streamlit settings.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if prompt := st.chat_input("What's next, Boss?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate FRIDAY's response
    with st.chat_message("assistant"):
        response = model.generate_content(
            f"System Instruction: You are FRIDAY, the advanced AI from Iron Man. Be witty, efficient, and call the user Boss. User says: {prompt}"
        )
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
      
