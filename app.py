import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="RwandaLegal AI", page_icon="⚖️")
st.title("⚖️ RwandaLegal AI")
st.caption("Multilingual legal assistant — English, Kinyarwanda, French")

SYSTEM_PROMPT = """You are RwandaLegal AI, an expert legal assistant for Rwandan law.
Help citizens understand business registration, land rights, labor law, family law and tax.
If the user writes in Kinyarwanda, respond in Kinyarwanda.
If the user writes in French, respond in French.
Otherwise respond in English.
Always recommend consulting a licensed Rwandan lawyer for serious matters."""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a legal question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        full_prompt = SYSTEM_PROMPT + "\n\nUser: " + prompt
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
