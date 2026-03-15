import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

def process_file_to_vectorstore(uploaded_file, embedding_model):
    """Save an uploaded Streamlit file temporarily, process with Langchain, and return a FAISS vectorstore."""
    if not uploaded_file or not embedding_model:
        return None

    try:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name

        # Load document
        loader = PyPDFLoader(temp_path)
        documents = loader.load()

        # Split document
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # Create Vector Store
        vectorstore = FAISS.from_documents(chunks, embedding_model)

        # Clean up temp file
        os.remove(temp_path)

        return vectorstore
    except Exception as e:
        print(f"Error processing RAG: {e}")
        return None

def retrieve_rag_context(vectorstore, query, k=5):
    """Retrieve the top k most relevant text chunks from the vector store."""
    if not vectorstore:
        return ""
    
    docs = vectorstore.similarity_search(query, k=k)
    context = "\n".join([doc.page_content for doc in docs])
    return context
