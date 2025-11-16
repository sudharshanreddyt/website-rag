from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()

def load_website(url: str) -> List[Document]:
    """Fetch website HTML and extract text."""
    loader = WebBaseLoader(web_paths=[url])
    docs = loader.load()
    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    """Split website content into manageable text chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap = 100,
        add_start_index = True
    )

    all_splits = text_splitter.split_documents(docs)
    return all_splits


def embed_documents(splitted_docs: List[Document]):
    """Embed text chunks and store them in Chroma."""
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        collection_name="website_chunks",
        embedding_function=embeddings,
        persist_directory=None
    )

    vector_store.add_documents(splitted_docs)
    return vector_store


def prompt_with_context(query, vector_store):
    """Retrieve context and build the final prompt for the LLM."""

    retrieved_docs = vector_store.similarity_search(query, k = 2)
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    sys_prompt = f"""
    You are a helpful assistant. Use ONLY the website information provided below to answer the question.
    Keep your answer concise (max 10 lines). 
    Context : {docs_content}
    Question : {query}
    Answer:
    """
    return sys_prompt


