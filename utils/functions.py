
# import validators
# import requests
import base64
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import hashlib
from datetime import datetime
import pytz
from docx import Document
import os
import fitz
from db import *
import numpy as np
from io import BytesIO
load_dotenv()

def enocode_image(user_img):
    try:
       
        base64_image = base64.b16encode(user_img.read()).decode("utf_8")
        return base64_image
    # except FileNotFoundError:
    #     return f"file not found Error {user_img}"
    except Exception as e:
        return e

def decode_image(user_img):
    try:
        decoded_image = base64.b64decode(user_img)
        return decoded_image
    except FileNotFoundError:
        return f"file not found Error {user_img}"
    except Exception as e:
        return e

def hash_values(user_id, email,id,curr_user):
    # Create a unique string to hash
    unique_string = f"{user_id}:{email}:{id}:{curr_user}"
    # Create a SHA-256 hash of the unique string
    # hashed_value = hashlib.sha256(unique_string.encode()).hexdigest()
    encoded_value = base64.urlsafe_b64encode(unique_string.encode()).decode('utf-8')
    return encoded_value




def encodeJwt(data):
    encoded_bytes = base64.b64encode(data.encode('utf-8'))   
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decodedata(data):
    decoded_bytes = base64.b64decode(data)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

import secrets
    
def generate_api_key():
    return secrets.token_urlsafe(32)

import random

def generate_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp


def verify_expiry(expirytime):
    utc = pytz.UTC
    curnt_time = datetime.now()
    dt_string = str(expirytime)
    new_dt = dt_string[:19]
    curnt_time = datetime.strptime(str(curnt_time), '%Y-%m-%d %H:%M:%S.%f')
    expire_ts = datetime.strptime(new_dt, '%Y-%m-%d %H:%M:%S')
    month_name = expirytime.strftime("%d")+" "+expirytime.strftime("%b") +" "+expirytime.strftime("%Y")
    time = expirytime.strftime("%H")+":"+expirytime.strftime("%M")
    curnt_time = curnt_time.replace(tzinfo=utc)
    expire_ts = expire_ts.replace(tzinfo=utc)
    return curnt_time,expire_ts


def create_reset_token(email: str):
    to_encode = {"sub": email}
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")

ls=[]

def extract_text_from_docx(file_bytes: bytes):
    try:
        doc = Document(BytesIO(file_bytes))
        lines = [p.text for p in doc.paragraphs if p.text.strip()]
        # print(lines)
        return "\n".join(lines)
    except Exception as e:
        return f"The File has error: {e}"

def extract_text_from_pdf(filename):
    try:
        doc = fitz.open(stream=filename, filetype="pdf")  # use stream for BytesIO
        text = []
        for page in doc:
            page_text = page.get_text().replace("\n", " ")
            text.append(page_text)
        return " ".join(text)  # or "\n".join(text) if you prefer line breaks
    except Exception as e:
        print(f"The File has error: {e}")
        return "The File has error: {e}"

