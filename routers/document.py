from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.document_upload_request import DocumentUploadRequest
from retrievers.retriever import retriever
from retrievers.retriever_provider import RetrieverProvider

router = APIRouter(prefix="/document", tags=["document"])

def connect_retriever() -> RetrieverProvider:
    raise NotImplementedError()

@router.post("/upload")
async def create_document_index_from_urls(request: DocumentUploadRequest):
    try:
        retriever.create_document_index_from_web_urls(
            collection_name=request.collection_name,
            urls=request.urls
        )

        return JSONResponse(
            content={ "data": "uploaded", "error": None },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={ "data": None, "error": str(e) },
            status_code=400
        )
