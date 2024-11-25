from tabnanny import check
from fastapi import FastAPI, UploadFile
import json
import uvicorn
import vector_store_func as vsf
import os


app=FastAPI()

@app.post("/create_database")
async def create_database(file:UploadFile):
     
    content = await file.read()
    data = json.loads(content)

    check = {}
    for category, items in data.items():
        # Store 0 if the dictionary is empty, 1 if it has keys
        if isinstance(items, dict) and len(items) == 0:
            check[category] = 0  # Empty dictionary
        else:
            check[category] = 1  # Dictionary has keys 
    
    file.file.seek(0)

    skill_documents=[]
    certification_documents=[]
    experience_documents=[]

    if check["Skills"]==1:
        skill_documents = await vsf.load_user_skills(file)
    
    if check["Certifications"]==1:
         certification_documents = await vsf.load_user_certifications(file)
    
    if check["Experience"]==1:
         experience_documents = await vsf.load_user_experience(file)

    all_user_documents = []
    
    for document in skill_documents:
        all_user_documents.append(document)
    for document in certification_documents:
        all_user_documents.append(document)
    for document in experience_documents:
        all_user_documents.append(document)
    
    print(all_user_documents)

    name_of_file_without_extension = os.path.splitext(file.filename)[0]
    vsf.create_user_database(all_user_documents , name_of_file_without_extension)
    return "Database Created"






