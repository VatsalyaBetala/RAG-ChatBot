import redis
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
import config
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

REDIS_CHAT_HISTORY_KEY = "chatbot:history"

def store_chat_history(user_input, chatbot_response):
    redis_client.rpush(REDIS_CHAT_HISTORY_KEY, user_input)
    redis_client.rpush(REDIS_CHAT_HISTORY_KEY, chatbot_response)

def load_chat_history():
    """ 
    This function loads the chat history from Redis. 
    It also formats it for Streamit in JSON format that is accepted by it.
    """
    
    history = redis_client.lrange(REDIS_CHAT_HISTORY_KEY, 0, -1)
    formatted_history = []
    
    for i in range(0, len(history), 2):
        if i + 1 < len(history):
            user_message = history[i].replace("User: ", "").strip() 
            bot_message = history[i + 1].replace("Bot: ", "").strip()
            
            formatted_history.append({"role": "user", "content": user_message})
            formatted_history.append({"role": "assistant", "content": bot_message})
    
    return formatted_history

def clear_chat_history():
    redis_client.delete(REDIS_CHAT_HISTORY_KEY)

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
    """Handles user queries, stores responses, and retrieves history."""
    qa_chain = load_chatbot()
    chat_history = load_chat_history()
    chat_history.append(HumanMessage(content=query))

    response = qa_chain.invoke({"question": query, "chat_history": chat_history})
    answer = response['answer']

    store_chat_history(query, answer)

    sources = "\n\n---\n\n".join([doc.page_content[:500] for doc in response.get('source_documents', [])])
    
    return answer, sources

