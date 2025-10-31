from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings #working

# for using pdfloader
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

#extracting text from pdf
def get_pdf_text(pdf_files: list):
    text = ""
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, 
        chunk_overlap=40
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001');
    metadatas = [{"source": f"chunk-{i+1}"} for i in range(len(text_chunks))]
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings, metadatas= metadatas)
    vector_store.save_local("faiss_index")
    return "Vector store created and saved locally."

def load_vector_store():
    embeddings = embeddings = GoogleGenerativeAIEmbeddings(model='models/gemini-embedding-001');
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True )
    return vector_store
