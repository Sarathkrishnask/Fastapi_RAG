
"""
UTIls import
"""
from utils.functions import extract_text_from_docx,extract_text_from_pdf
from utils.mongo_ import save_mongo,fetch_data,list_docs
from utils.rag import rag_response

"""
Other python imports
"""

from dotenv import load_dotenv
from typing import *
from utils.logging_config import logger
load_dotenv()

async def list_filename():
    logger.info("list_filename called")
    try:
        result = list_docs()
        logger.info(f"Documents fetched: {result}")
        print(result, "==========================================")
        return True, result
    except Exception as e:
        logger.error(f"Error in list_filename: {str(e)}")
        return False, str(e)


async def upload_file(file, current_user):
    logger.info(f"upload_file called by {current_user} for file: {file.filename}")
    try:
        filename = file.filename.lower()
        content_type = file.content_type

        if filename.endswith(".pdf") or content_type == "application/pdf":
            logger.info("PDF file detected")
            file_bytes = await file.read()
            text = extract_text_from_pdf(file_bytes)
            save_mongo(current_user, filename, text)
            logger.info("PDF content saved to MongoDB")
            return True, {"type": "pdf", "content": text, "current_user": current_user}

        elif filename.endswith(".docx"):
            logger.info("DOCX file detected")
            file_bytes = await file.read()
            text = extract_text_from_docx(file_bytes)
            save_mongo(current_user, filename, text)
            logger.info("DOCX content saved to MongoDB")
            return True, {"type": "pdf", "content": text, "current_user": current_user}

        else:
            logger.warning(f"Unsupported file type: {filename}")
            return False, "Unsupported file type" 

    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return False, f"Error occurred: {str(e)}"


async def query_rag(query: str, user_id: int, filename: str): 
    logger.info(f"query_rag called with user_id={user_id}, filename={filename}")
    try:
        result = fetch_data(user_id, filename)
        logger.info("Fetched data for RAG processing")

        if not result or not isinstance(result, list):
            logger.warning("No document found or result is not a list")
            return False, "No document found or invalid data."

        print("Document loaded, running RAG...")
        logger.info("Running RAG response generation")
        end_result = await rag_response(result, query)
        logger.info("RAG response successfully generated")

        return True, end_result

    except Exception as e:
        logger.error(f"Error in query_rag: {e}")
        return False, f"Error occurred: {e}"
