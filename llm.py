import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()



def get_llm(model="openai/gpt-oss-120b"):
    return ChatGroq(
        model=model)

