from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
import config

def load_chatbot():
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(config.VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(model=config.LLM_MODEL, temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True 
    )

    return qa_chain


def ask_question(query):
    qa_chain = load_chatbot()
    response = qa_chain.invoke(query)
    answer = response['result']
    
    sources = "\n\n---\n\n".join(
        [doc.page_content[:500] for doc in response['source_documents']] 
    )

    return answer, sources 
