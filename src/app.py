from indexer import index_website
from rag_pipeline import ask
import streamlit as st
from vector_store import (
    get_collections
)
from pdf_indexer import index_pdf
import os


st.set_page_config(
    page_title="Chat with Any Website",
    page_icon="🌐"
)

# Page Config
st.title(
    "🧠 AI Knowledge Assistant"
)

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "source_loaded" not in st.session_state:
    st.session_state.source_loaded = False

if "current_source" not in st.session_state:
    st.session_state.current_source = None

# Sidebar for website input and indexing
with st.sidebar:

    st.header("Knowledge Integration Engine")

    source_type = st.radio(
        "Make a Pick",
        [
            "Website", 
            "PDF"
        ]

    )

    if source_type == "Website":
        
        url = st.text_input(
            "Enter Website url..."
        )

    else:
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

    process = st.button(
    "Process Source"
    )

    
    collections = get_collections()

    if collections:
        st.divider()

        st.subheader(
            "📚 Previously Indexed Sources"
        )

        for collection in collections:

            display_name = (
                collection
                .replace("_", ".")
            )

            if st.button(
                display_name,
                key=collection
            ):

                st.session_state.chat_history = []

                st.session_state.current_source = (
                    "https://"
                    +
                    display_name
                )

                st.session_state.source_loaded = True

                st.success(
                    f"Loaded {display_name}"
                )

    if process:

        if source_type == "Website":

            if not url:
                st.error(
                    "Please enter a URL."
                )

            else:
                st.session_state.chat_history = []
                st.session_state.source_loaded = False
                st.session_state.current_source = None

                try:
                    with st.spinner(
                        "Processing website..."
                    ):
                        index_website(url)

                    st.session_state.current_source = url
                    st.session_state.source_loaded = True

                    st.success(
                        "🌐 Website indexed successfully!"
                    )

                except Exception as e:
                    st.error(
                        f"Could not process website: {e}"
                    )
        
        if source_type == "PDF":

            if not uploaded_file:

                st.error(
                    "Please upload a PDF."
                )

            else:
                st.session_state.chat_history = []

                try:
                    with st.spinner(
                        "Processing PDF..."
                    ):
                        file_path = os.path.join(
                        "data",
                        "uploads",
                        uploaded_file.name
                    )

                    with open(file_path, "wb") as f:
                        f.write(
                            uploaded_file.getbuffer()
                        )
                        
                    index_pdf(file_path)

                    st.session_state.source_loaded = True

                    st.session_state.current_website = file_path

                    st.success(
                        "📄 PDF indexed successfully!"
                    )

                except Exception as e:
                    st.error(
                        f"Could not process PDF: {e}"
                    )

for role, message in (
    st.session_state.chat_history
):

    with st.chat_message(role):
        st.markdown(message)

question = st.chat_input(
    "Ask something..."
)

if question:

    if not st.session_state.source_loaded:
        st.warning(
            "Please process a source first."
        )

    else:

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner(
            "Thinking..."
        ):
            if not st.session_state.current_source:
                st.warning(
                    "Please process a source first."
                )
                        
            answer, sources = ask(
                question,
                st.session_state.chat_history,
                st.session_state.current_source
            )

        with st.chat_message("assistant"):

            st.markdown(answer)

            if sources:

                st.markdown("---")
                st.markdown("**Sources:**")

                with st.expander("Sources"):

                    for source in sources:

                        st.write(
                            source["source"]
                        )

        st.session_state.chat_history.append(
            ("user", question)
        )

        st.session_state.chat_history.append(
            ("assistant", answer)
        )

