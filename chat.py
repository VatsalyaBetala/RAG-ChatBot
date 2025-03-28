from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
import config
import os
from dotenv import load_dotenv

load_dotenv()

chat_history = [
    SystemMessage(content="You are an interactive Data Science coordinator. Answer students' questions.")
]

def load_chatbot():
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(config.VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model=config.LLM_MODEL, temperature=0)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain

def ask_question(query):
    global chat_history 

    qa_chain = load_chatbot()

    chat_history.append(HumanMessage(content=query))  

    response = qa_chain.invoke({"question": query, "chat_history": chat_history})
    
    answer = response['answer']
    chat_history.append(AIMessage(content=answer))  
    sources = "\n\n---\n\n".join(
        [doc.page_content[:500] for doc in response.get('source_documents', [])]
    )

    return answer, sources
