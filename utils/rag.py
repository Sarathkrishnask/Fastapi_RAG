import os
import re
import faiss
import numpy as np
from groq import Groq
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from typing import Dict, Optional
from utils.logging_config import logger
langchain_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


class InMemoryDocstore:
    """Docstore that stores documents in memory."""

    def __init__(self, _dict: Optional[Dict[str, Document]] = None):
        """Initialize with empty dictionary."""
        if _dict is None:
            _dict = {}
        self._dict = _dict

    def search(self, search_key: str) -> Document:
        """Search for a document by key."""
        return self._dict[search_key]

    def add(self, documents: Dict[str, Document]) -> None:
        """Add new documents to the store."""
        self._dict.update(documents)


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces/newlines
    return text.strip()


async def preprocess_text(texts):
    logger.info("Starting text preprocessing.")
    cleaned_texts = [clean_text(text) for text in texts]
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
    chunks = []
    for text in cleaned_texts:
        chunks.extend(splitter.split_text(text))
    
    logger.info(f"Preprocessing complete. Total chunks created: {len(chunks)}")
    return chunks


embedding_model = SentenceTransformer('all-mpnet-base-v2')


async def embed_texts(texts):
    logger.info("Starting embedding of texts.")
    embeddings = embedding_model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    logger.info("Text embedding completed.")
    return embeddings


async def save_to_faiss(embeddings, texts):
    logger.info("Saving embeddings to FAISS index.")
    index_to_docstore_id = {i: str(i) for i in range(len(texts))}
    docstore = InMemoryDocstore({str(i): Document(page_content=text) for i, text in enumerate(texts)})
    
    d = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(d)
    faiss_index.add(embeddings.astype(np.float32))
    
    vector_store = FAISS(langchain_embeddings, faiss_index, docstore, index_to_docstore_id)

    logger.info(f"Number of Documents in Vector Store: {len(vector_store.docstore._dict)}")
    return vector_store


api_key = "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"
client = Groq(api_key=api_key)


async def retrieve_and_answer(query, vector_store):
    logger.info(f"Running similarity search for query: {query}")
    docs = vector_store.similarity_search(query, k=3)
    
    doc_text = " ".join([doc.page_content for doc in docs])
    logger.debug(f"Retrieved Context: {doc_text}")
    
    prompt = f"""
    You are a helpful and accurate AI assistant designed to answer user queries based only on the context provided below.

    <context>
    {doc_text}
    </context>

    Instructions:
    - Use ONLY the context to answer the question.
    - Do NOT assume or generate information that is not clearly found in the context.
    Question: {query}
    """
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    logger.info("LLM response received.")
    logger.debug(f"Raw Completion Response: {completion}")
    response = completion.choices[0].message.content
    logger.info(f"Response: {response}")
    return response


async def rag_response(raw_texts, query):
    logger.info("Starting RAG pipeline.")
    texts = [item['pdf_raw_text'] for item in raw_texts]
    chunks = await preprocess_text(texts)
    
    embeddings = await embed_texts(chunks)
    vector_store = await save_to_faiss(embeddings, chunks)
    
    response = await retrieve_and_answer(query, vector_store)
    logger.info(f"Final Answer: {response}")
    return response
