# RAG Document Chatbot

Welcome to the **RAG Document Chatbot**! 🚀

This is a **retrieval-augmented generation (RAG)** chatbot that allows you to ask questions based on a document, and it provides **contextual answers**. Using a combination of **OpenAI GPT-4o**, **LangChain**, and **FAISS**, the chatbot can intelligently retrieve relevant parts of your document and use them to generate accurate answers.

---

### 🔧 **Tech Stack**

- **OpenAI GPT-4o**: For generating human-like answers.
- **LangChain**: To build a powerful and flexible pipeline for processing and querying documents.
- **FAISS**: For efficient similarity search and retrieval of relevant document chunks.
- **Streamlit**: For building a simple, interactive web interface.

---

### 📄 **How It Works**

1. **Ingesting Documents**:  
   The text from a `.txt` file is processed and split into **chunks**. Each chunk is then passed through an **embedding model** to create a **vector representation**, for semantic search.
   
2. **Storing Chunks**:  
   The chunks are stored in **FAISS** for fast and efficient similarity search. This allows us to retrieve the most relevant chunks when a user asks a question. This is done because the models have a limited context window, and it proves to be expensive to feed all the data from the document together. 

3. **Querying the Document**:  
   When a user asks a question, the chatbot uses **semantic search** to retrieve the most relevant chunks. These chunks are then passed to **GPT-4o** to generate a response based on the retrieved context.

4. **Streamlit Interface**:  
   The chatbot is exposed through a **Streamlit web app**, where users can input their questions and get instant answers, along with context showing which parts of the document were used.

---

### 📋 **How to Run the App**

1. **Clone the Repository**:

```bash
git clone https://github.com/your-username/RAG-Document-Chatbot.git
cd RAG-Document-Chatbot
```

2. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

3. **Add Your Document**:  
   Place your `.txt` file (the document you want to query) in the `data` folder. Make sure the file path in `config.py` matches the location of your file.

4. **Run the Ingest Script**:  
   This will process your document, create chunks, generate embeddings, and save them in FAISS.

```bash
python ingest.py
```

5. **Start the Streamlit App**:

```bash
streamlit run app.py
```

Now, open your browser and go to `http://localhost:8501` to interact with the chatbot.

---

### 🌱 **Future Directions**

While this project currently handles basic querying and document interaction, there are plenty of opportunities for improvement:

- **Multilingual Support**: Extend the chatbot to handle documents in multiple languages.
- **More Data Sources**: Support for PDF, Word, and other document types.
- **Contextual Memory**: Implement a memory feature where the chatbot can remember previous interactions in a conversation.
- **User Customization**: Allow users to upload their own documents and have the chatbot process them in real time.

---
