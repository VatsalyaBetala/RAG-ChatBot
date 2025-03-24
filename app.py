import streamlit as st
from chat import ask_question

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("📚 Ask Your Document")

st.markdown("Type a question based on your uploaded document:")

query = st.text_input("💬 Your question")

if query:
    with st.spinner("Thinking... 🤔"):
        try:
            answer, context = ask_question(query)

            st.markdown("### Answer")
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by OpenAI + LangChain + FAISS")
