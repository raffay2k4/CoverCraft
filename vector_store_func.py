from langchain.document_loaders import JSONLoader
import jq
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
import re
from fastapi import UploadFile, File
import os
import json


db_folder_path = "D:\Atomcamp\CoverCraft\database"

embedding_model = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key="iiYtqoN8hTQ2EcoeV6FyeOqkT6wdvjFurq39gqMm")

async def load_user_skills(file : UploadFile = File(...)):
    #Save the uploaded file temporarily
    upload_path="D:\\Atomcamp\\CoverCraft\\temp"
    file_path = os.path.join(upload_path, file.filename)

    file_contents_bytes = await file.read()
    file_contents_str = file_contents_bytes.decode('utf-8')

    with open(file_path, "w") as f:
        f.write(file_contents_str)

    file.file.seek(0)

    skills_loader = JSONLoader(file_path=file_path, jq_schema=".Skills[]", text_content=False)
    skills_documents = skills_loader.load()
    return skills_documents

async def load_user_certifications(file:UploadFile):
    # Save the uploaded file temporarily
    upload_path="D:\\Atomcamp\\CoverCraft\\temp"
    file_path = os.path.join(upload_path, file.filename)

    file_contents_bytes = await file.read()
    file_contents_str = file_contents_bytes.decode('utf-8')

    with open(file_path, "w") as f:
        f.write(file_contents_str)

    file.file.seek(0)

    certifications_loader = JSONLoader(file_path=file_path, jq_schema=".Certifications[]", text_content=False)
    certifications_documents = certifications_loader.load()
    return certifications_documents

async def load_user_experience(file:UploadFile):

    # Save the uploaded file temporarily
    upload_path="D:\\Atomcamp\\CoverCraft\\temp"
    file_path = os.path.join(upload_path, file.filename)
    
    file_contents_bytes = await file.read()
    file_contents_str = file_contents_bytes.decode('utf-8')

    with open(file_path, "w") as f:
        f.write(file_contents_str)

    file.file.seek(0)

    experience_loader = JSONLoader(file_path=file_path, jq_schema=".Experience[]", text_content=False)
    experience_documents = experience_loader.load()
    return experience_documents 

def create_user_database(data:list, name: str):
    db_path= f"{db_folder_path}\{name}"
    vector_store=Chroma.from_documents(documents=data, embedding=embedding_model, persist_directory = db_path)

def load_user_database(name:str):
    db_path= f"{db_folder_path}\{name}"
    u_database = Chroma(persist_directory=db_path, embedding_function=embedding_model)
    return u_database

def extract_user_context(user_database:Chroma, message:str):
    documents_list = user_database.similarity_search(message)
    list_of_extracted_document_strings=[]

    for document in documents_list:
        page_content = document.page_content
        list_of_extracted_document_strings.append(page_content)

    return list_of_extracted_document_strings

    


