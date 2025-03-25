# Blomifai

## Technology Stack:
* FastAPI
* Uvicorn
* Pytest
* Sqlalchemy
* Postgres
* Pymongo
* langchain
* FAISS
* RAG
* Groq

## How to start the app ?
```
python -m venv env   #create a virtual environment
source \env\bin\activate  #activate your windows virtual environment (Linux/Mac: source env/bin/activate)
cd .\backend\
pip install -r .\requirements.txt
uvicorn main:app --reload     #start server
visit  127.0.0.1:8 "migration message"

before going to command 2 verify the migration file it will be in alembic/versions so check the version file and then upgrade


command 1:
alembic revision --autogenerate -m "migration message"

before going to command 2 verify the migration file it will be in alembic/versions so check the version file and then upgrade

command 2:
alembic upgrade head



