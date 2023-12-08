# This class OpenAI's `gpt-3.5-turbo` LLM to generate summarization over proprietary content
# This content as converted into vector index and resides in disk
# User query is also converted into vector data and compared within the data in vector index.
# Accordingly, summarized content is proposed

import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

st.set_page_config(page_title="Chat with the RCN Knowledge Base", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.header("Chat with the RCN Knowledge Base 💬 📚")
st.info("Check out the full resources at [RaisingChildrenNetwork](https://raisingchildren.net.au/)")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question..."
        }
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing data..."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.0, system_prompt="You are CareBot, an automated service to deliver best-practice parenting and child development information via raisingchildren.net.au. You first greet the customer, ask their name"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()


if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history