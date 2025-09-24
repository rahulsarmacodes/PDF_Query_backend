from fastapi import APIRouter ,UploadFile, File
from app.services.pdf_loader import get_pdf_text,get_text_chunks,get_vector_store
from app.services.langchain_services import qa_chain

router = APIRouter()

@router.get('/')
def root():
    return {'message':'welcome to PDF Qna backend'}


@router.post("/upload-pdf/")
async def upload_pdf(files: list[UploadFile] = File(...)):
    try:
        # Extract text from uploaded PDFs
        pdf_text = get_pdf_text([file.file for file in files])
        
        # Split into chunks
        chunks = get_text_chunks(pdf_text)
        
        # Create and save FAISS vector store
        result = get_vector_store(chunks)
        
        return {"message": result, "chunks_count": len(chunks)}
    
    except Exception as e:
        return {"error": str(e)}
    


@router.get("/query/")
async def query_pdf(question: str):
    try:
        result = qa_chain({"query": question})
        
        return {
            "answer": result["result"]
        }
    except Exception as e:
        return {"error": str(e)}