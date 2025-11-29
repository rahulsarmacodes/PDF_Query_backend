from fastapi import APIRouter ,UploadFile, File, Depends
from app.services.pdf_loader import get_pdf_text,get_text_chunks,get_vector_store
from app.services.langchain_services import qa_chain, clear_memory
from langchain_community.vectorstores import Chroma
from langchain_cohere import CohereEmbeddings
from app.auth.auth import get_current_user

router = APIRouter()



@router.post("/upload-pdf/")
async def upload_pdf(
    files: list[UploadFile] = File(...), user: dict = Depends(get_current_user)):
    try:
        # Extract text from uploaded PDFs
        pdf_text = get_pdf_text([file.file for file in files])
        
        # Split into chunks
        chunks = get_text_chunks(pdf_text)
        
        result = get_vector_store(chunks)
        
        return result
    
    except Exception as e:
        return {"error": str(e)}
    


@router.get("/query/")
async def query_pdf(question: str):
    try:
        chain = qa_chain()
        result = chain.invoke({"question": question})
        
        return {
            "answer": result["answer"]
        }
    except Exception as e:
        return {"error": str(e)}
    

@router.delete("/clear-embeddings/")
async def clear_embeddings(user: dict = Depends(get_current_user)):
    try:

        #clear history stored in memory
        clear_memory()

        # Load same embedding model you used during creation
        embeddings = CohereEmbeddings(model="embed-multilingual-v3.0")

        # Load vector store with existing persisted data
        vector_store = Chroma(
            persist_directory='my_chroma_db',
            collection_name='sample',
            embedding_function=embeddings
        )
        collection = vector_store._collection

       # fetch all stored ids
        all_items = collection.get(include=[])
        ids = all_items.get("ids", [])

        #Delete only if IDs exist
        if ids:
            collection.delete(ids=ids)

        return {
            "status": "success",
            "deleted_vectors": len(ids),
            "message": "All embeddings deleted from Chroma 'sample' collection / conversation history deleted from memory.",
        }

    except Exception as e:
        return {"error": str(e)}