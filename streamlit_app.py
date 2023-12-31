# This class OpenAI's `gpt-3.5-turbo` LLM to generate summarization over proprietary content
# This content as converted into vector index and resides in disk
# User query is also converted into vector data and compared within the data in vector index.
# Accordingly, summarized content is proposed
# This class also remembers history between a user and the AI

import streamlit as st
import openai
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter


st.set_page_config(page_title="Chat with the RCN Knowledge Base", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.header("Chat with the RCN Knowledge Base 💬 📚")
st.info("Check out the full resources at [RaisingChildrenNetwork](https://raisingchildren.net.au/)")

llm_name = "gpt-3.5-turbo-0301"
chat_history = []

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question..."
        }
    ]

# Initializes memory
def memory():
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    return memory

@st.cache_resource(show_spinner=False)
def load_data(file, chain_type, k):
    with st.spinner(text="Loading and indexing data..."):
        # 1. Loads data
        loader = CSVLoader(file_path=file)
        documents = loader.load()

        # 2. Selects embeddings
        embeddings = OpenAIEmbeddings()

        # 3. Chunkify data
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.split_documents(documents)
        db = DocArrayInMemorySearch.from_documents(docs, embeddings)

        # 4. Defines retriever
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})

        # 5. Creates chatbot chain. Memory is managed externally
        qa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name=llm_name, temperature=0),
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=True,
            return_generated_question=True,
            # memory=memory,
        )
        return qa

file = 'data/toddlers_sleep.csv'
index = qa = load_data(file, "stuff", 4)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = qa({"question": prompt, "chat_history": chat_history})
            response = result["answer"]
            chat_history.extend([(prompt, response)])
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history


















