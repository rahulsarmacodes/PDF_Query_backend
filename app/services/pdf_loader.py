from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Gemini embeddings
from langchain_cohere import CohereEmbeddings # cohere embeddings(working better)

from langchain_community.document_loaders import PyPDFLoader # to implement later

load_dotenv()

# 1. Extract text from PDF

def get_pdf_text(pdf_files: list):
    text = ""
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


# 2. Split text into chunks

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30
    )
    chunks = text_splitter.split_text(text)
    return chunks


# 3. Create and save Chroma Vector Store

def get_vector_store(text_chunks):
    embeddings = CohereEmbeddings(model='embed-multilingual-v3.0')
    metadatas = [{"source": f"chunk-{i+1}"} for i in range(len(text_chunks))]

    vector_store = Chroma.from_texts( 
        texts=text_chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory='my_chroma_db',
        collection_name='sample' )

    return {
        "message":"Vector store created and saved locally in 'my_chroma_db'.",
        "metadata": metadatas,
        "chunk_size":len(text_chunks)
    }

# 4. Load existing Chroma Vector Store
def load_vector_store():
    embeddings = CohereEmbeddings(model='embed-multilingual-v3.0')
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory='my_chroma_db',
        collection_name='sample'
    )
    return vector_store
