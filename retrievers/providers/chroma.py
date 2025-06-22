from config.settings import settings

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb import DEFAULT_TENANT, DEFAULT_DATABASE
from models.retriever_settings import RetrieverSettings
from retrievers.retriever_provider import RetrieverProvider
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from chromadb.config import Settings
import chromadb
from config.settings import settings

class ChromaDB(RetrieverProvider):
    """ChromaDB client for vector storage and retrieval."""
    
    def __init__(self):
        super().__init__()
    
    def create(self, settings:RetrieverSettings):
        self.embedding_model_name = settings.embedding_model_name
        self.collection_name = settings.collection_name
        self.persist_directory = settings.persist_directory
        self.retriever = None
        self.collection = None
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={"device": settings.chroma_device},
        )
        
    def create_document_index_from_web_urls(self,
        collection_name: str = settings.chroma_collection,
        urls: list[str] = [],
    ):
        # Load
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        # Sprint
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            AutoTokenizer.from_pretrained(self.embedding_model_name, token=settings.hf_token),
            chunk_size=500,
            chunk_overlap=50,
            # add_start_index=True,
            # strip_whitespace=True,
        )
        doc_splits = text_splitter.split_documents(docs_list)

        vectordb = Chroma.from_documents(
            documents=doc_splits,
            collection_name=collection_name,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            # client_settings={
            #     "host": settings.chroma_host,
            #     "port": settings.chroma_port,
            #     "ssl": settings.chroma_ssl,
            #     "tenant": DEFAULT_TENANT,
            #     "database": DEFAULT_DATABASE
            # }
        )
        
        self.retriever = vectordb.as_retriever()
        
    def create_collection(self, 
        embedding_model_name: str = settings.chroma_embeddings_model,
        collection_name: str = settings.chroma_collection,
    ):
        self.client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
            ssl=settings.chroma_ssl,
            headers=None,
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )
        
        print(self.client.list_collections())
        
        self.model = SentenceTransformer(embedding_model_name)
        self.collection = self.client.get_or_create_collection(collection_name)
        
    def similarity_search(self, query: str, top_k: int) -> list[dict]:
        result = []
        # docs_with_scores = self.retriever.vectorstore.similarity_search_with_score(query, k=top_k)
        # for doc, score in docs_with_scores:
        #     result.append({
        #         "content": doc.page_content,
        #         "metadata": doc.metadata,
        #         "score": score
        #     })
        # return result
        
        query_embedding = self.model.encode([query])[0]
        results = self.collection.query(query_embeddings=[query_embedding], n_results=3)
        
        print("\nTop 3 similar documents:")
        for i in range(len(results["documents"][0])):
            data = {
                "ids": results['ids'][0][i],
                "score": results['distances'][0][i],
                "doc": results['documents'][0][i][:100],
                "metadatas": results['metadatas'][0][i],
            }
            
            # result.append(data)
            
            print(f'\nScore: {data.get("score", 0.00000):.4f}')
            print(f'ID: {data.get("ids")}')
            print(f'Doc: {data.get("doc")}...')
            print(f'Metadatas: {data.get("metadatas")}...')
            
        return results

