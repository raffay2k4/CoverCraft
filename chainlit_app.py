import chainlit as cl
import chatbot as cb
import vector_store_func as vsf

sel_database=None
chain=cb.coverletter_chain

@cl.set_chat_profiles
async def chat_profiles():
    profiles = []
    profiles = await cb.load_chatbot_profiles(profiles)
    return profiles


@cl.on_chat_start
async def on_chat_start():
    selected_chat_profile=cl.user_session.get("chat_profile")
    await cl.Message(content=f"You have selected {selected_chat_profile}'s CoverCraft").send()

    cb.chat_history=[]
    global sel_database

    sel_database = vsf.load_user_database(selected_chat_profile)
    await cl.Message(content=f"{selected_chat_profile}'s Database Loaded Successfully.").send()

@cl.on_message
async def on_message(message: cl.Message):
    context = vsf.extract_user_context(sel_database, message.content)

    user_input= {
        "chat_history": cb.chat_history,
        "context":context,
        "input":message.content
    }

    await cb.run_chatbot(user_input,chain)