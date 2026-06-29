from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv()


@st.cache_resource
def load_llm():

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )


llm = load_llm()