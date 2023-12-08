import streamlit as st
import openai
# from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from IPython.display import display, Markdown
from langchain.document_loaders import UnstructuredMarkdownLoader
from llama_index import SimpleDirectoryReader

st.set_page_config(page_title="Chat with the RCN Knowledge Base", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.header("Chat with the RCN Knowledge Base 💬 📚")
st.info("Check out the full resources at [RaisingChildrenNetwork](https://raisingchildren.net.au/)")

llm_model = "gpt-3.5-turbo-0301"
llm = ChatOpenAI(temperature=0.0, model=llm_model) # Ensure OPENAI_API_KEY is set in the environment variable

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question..."
        }
    ]

# Function for generating LLM response
# Custom function, as defined by streamlit, for taking in user's input prompt as an argument to generate an AI response using the ChatOpenAI
#   method (this LLM model can be swapped with any other one)
# Refer https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/
def generate_response(query):
    response = index.query(query, llm=llm)
    return response

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing data..."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        embeddings = OpenAIEmbeddings()

        index = VectorstoreIndexCreator(
            vectorstore_cls=DocArrayInMemorySearch,
            embedding=embeddings,
        ).from_loaders([loader])
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
            # response = st.session_state.chat_engine.chat(prompt)
            response = generate_response(prompt)
            st.write(response) 
            # st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history