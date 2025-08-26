import streamlit as st
import requests
import json
import streamlit as st

API_ENDPOINT = st.secrets['api_endpoint']  
ACCESS_CODE = st.secrets['access_code']

st.set_page_config(page_title="NLBike Assistant", page_icon="🚴", layout="centered")

# ---------------------------
# Session State Management
# ---------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# Login Page
# ---------------------------
if not st.session_state.authenticated:
    st.title("🔐 Enter Access Code")
    code = st.text_input("Access Code", type="password")
    if st.button("Submit"):
        if code == ACCESS_CODE:
            st.session_state.authenticated = True
            st.success("Access granted!")
            st.rerun()
        else:
            st.error("Incorrect code. Try again.")
    st.stop()

# ---------------------------
# Main Assistant Page
# ---------------------------
st.title("🚴 NLBike Analytics Assistant")

st.markdown("Ask me anything about NL Bike Share data!")

# Input box for question
question = st.text_input("Type your question and press Enter:", placeholder="e.g. How many kilometres were ridden by women on rainy days in June 2025?")

if question:
    st.chat_message("user").markdown(question)
    st.session_state.chat_history.append({"role": "user", "content": question})

    # ---------------------------
    # Stream API Response
    # ---------------------------
    with st.chat_message("assistant"):
        full_response = ""
        response_area = st.empty()

        try:
            with requests.post(API_ENDPOINT, json={"question": question}, stream=True) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))
                        token = data.get("answer", "")
                        full_response += token
                        response_area.markdown(full_response + "▌")  
        except Exception as e:
            response_area.error(f"⚠️ Error: {str(e)}")
        else:
            response_area.markdown(full_response.strip()) 
            st.session_state.chat_history.append({"role": "assistant", "content": full_response.strip()})

# ---------------------------
# Chat History (Optional)
# ---------------------------
with st.expander("💬 Chat History"):
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")
