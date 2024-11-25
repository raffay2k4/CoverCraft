import chainlit as cl
import prompts
import os
from langchain_cohere import ChatCohere
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import vector_store_func as vsf
import tools

icon = "https://static.vecteezy.com/system/resources/thumbnails/000/547/370/small/mail-02.jpg"
chat_history=[]

llm=ChatCohere(
    model="command-r-plus",
    temperature=0.3
)

coverletter_chain = (
    prompts.coverletter_prompt
    | llm
)

async def load_chatbot_profiles(profiles : list):
 # Iterate over all items in the database directory
    for item in os.listdir(vsf.db_folder_path):
        item_path = os.path.join(vsf.db_folder_path, item)
        if os.path.isdir(item_path):
            profiles.append(cl.ChatProfile(name= f"{item}", markdown_description=f"{item}s CoverCraft", icon = icon))
    
    return profiles

async def run_chatbot(user_input: dict, chain: Runnable):
    response = cl.Message(content="")

    for token in chain.stream(user_input):
        await response.stream_token(token.content)
    
    await response.send()

    chat_history.extend(
        [
            HumanMessage(content=user_input["input"]),
            AIMessage(content=response.content)
        ]
    )

   
