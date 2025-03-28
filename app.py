import streamlit as st
from chat import ask_question

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("🤖 RAG ChatBot")

st.markdown("Ask questions related to the **Data Science curriculum**.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Type your question here...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking... 🤔"):
        try:
            answer, context = ask_question(query)

            st.session_state.messages.append({"role": "assistant", "content": answer})

            with st.chat_message("assistant"):
                st.markdown(answer)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by OpenAI + LangChain + FAISS")
