import streamlit as st
from langchain_helper import load_website, split_documents, embed_documents, prompt_with_context
from langchain.chat_models import init_chat_model

st.set_page_config(
    page_title="Website RAG",
    page_icon="🔎",
    layout="centered"
)

@st.cache_resource
def load_model():
    return init_chat_model(model="openai/gpt-oss-120b", model_provider="groq")

model = load_model()

def stream_llm_response(prompt: str):
    """Streams model output into the UI."""
    st.write("### Answer")
    collected_data = ""
    response_placeholder = st.empty()

    for chunk in model.stream(prompt):
        text = chunk.content
        collected_data += text
        response_placeholder.write(collected_data)


st.title("🔎 Website RAG: Ask questions about any website")

website_url = st.text_input("Enter the website URL", placeholder="https://example.com")

if st.button("Load Website"):
    if website_url.strip():

        with st.spinner("Processing website..."):
            status_message = st.empty()

            status_message.write("Loading Website...")
            docs = load_website(website_url)

            status_message.write("Splitting Documents...")
            split_docs = split_documents(docs)

            status_message.write("Embedding Documents...")
            vector_store = embed_documents(split_docs)

        st.session_state["vector_store"] = vector_store
        status_message.write("")

        st.success("Website loaded and indexed successfully!")


question = st.text_input("Ask a question about the website:")

if st.button("Get Answer"):
    if "vector_store" not in st.session_state:
        st.error("Please load a website first.")

    elif question.strip(): 
        with st.spinner("Generating answer..."):
            vector_store = st.session_state["vector_store"]
            prompt = prompt_with_context(question, vector_store)
            stream_llm_response(prompt)

