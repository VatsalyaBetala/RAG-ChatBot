import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import config

def ingest_data():
    file_path = config.TXT_FILE_PATH

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            content = f.read()

    print(f"Loaded file: {file_path}")

    doc = Document(page_content=content, metadata={"source": os.path.basename(file_path)})

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents([doc])
    print(f"Total chunks created: {len(chunks)}")

    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local(config.VECTORSTORE_DIR)
    print("Embeddings saved to FAISS.")

ingest_data()