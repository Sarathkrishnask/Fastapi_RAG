from pymongo import MongoClient
import uuid
import os
from core.config import settings
from utils.logging_config import logger
# Setup
try:
    client = MongoClient("mongodb://localhost:27017")
    client.server_info()  # Forces a call to check connection
    db = client["rag-project"]
    collection = db["document_chunks"]
    print("✅ MongoDB connected")
except Exception as e:
    print(" Error:", e)


def list_docs():
    try:
        mongo_docs = list(collection.find({}, {"user_id": 1, "pdf_raw_text": 1, "document_name": 1}))
        if not mongo_docs:
            print("⚠️ No documents found.")
            logger.warning("⚠️ No documents found.")
            return []

        raw_texts = [
            {
                "user_id": doc["user_id"],
                "pdf_raw_text": doc.get("pdf_raw_text", ""),
                "document_name": doc["document_name"]
            }
            for doc in mongo_docs
        ]

        logger.info(f"📄 {len(raw_texts)} documents retrieved from MongoDB.")
        return raw_texts

    except Exception as e:
        print(f" Error fetching data from MongoDB: {e}")
        logger.error(f"Error fetching data from MongoDB: {e}")
        return []


def fetch_data(USER_ID, FILENAME):
    try:
        mongo_docs = list(collection.find({"user_id": USER_ID, "document_name": FILENAME}, {"user_id": 1, "pdf_raw_text": 1, "document_name": 1}))

        if not mongo_docs:
            print("⚠️ No documents found for user and filename.")
            logger.warning("⚠️ No documents found for user and filename.")
            return []

        raw_texts = [
            {
                "user_id": doc["user_id"],
                "pdf_raw_text": doc.get("pdf_raw_text", ""),
                "document_name": doc["document_name"]
            }
            for doc in mongo_docs
        ]

        logger.info(f"📄 {len(raw_texts)} documents fetched for user_id={USER_ID}, filename={FILENAME}")
        return raw_texts

    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")
        logger.error(f"Error fetching data from MongoDB: {e}")
        return []


def save_mongo(id, file_name, raw_data):
    documents = []
    try:
        documents.append({
            "id": f"DOC_{uuid.uuid4().hex[:6]}",
            'user_id': id,
            'document_name': file_name,
            'pdf_raw_text': raw_data,
        })
    except Exception as e:
        logger.error(f"Error in generating document: {e}")
        return f"Error in generating embeddings: {e}"

    try:
        collection.insert_many(documents)
        data = documents[0]["pdf_raw_text"]
        print("Chunked embeddings saved to MongoDB.", documents)
        logger.info(f"✅ Chunked embeddings saved to MongoDB for user_id={id}, file={file_name}")
        return f" Chunked embeddings saved to MongoDB. {data}"
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")
        logger.error(f"Error inserting into MongoDB: {e}")
        return f" Error inserting into MongoDB: {e}"
