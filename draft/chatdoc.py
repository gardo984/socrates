
import streamlit as st
import ollama
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_classic.retrievers import MultiQueryRetriever


st.title("Chat with Document")
uploaded_file = st.file_uploader("Upload file:", type=["txt", "pdf", "docx"])
add_file = st.button("Process File")

if uploaded_file and add_file:
    with st.spinner("Reading, chucking and embedding file..."):
        file_bytes = uploaded_file.read()
        filename = os.path.join("./", uploaded_file.name)
        with open(filename, 'wb') as f:
            f.write(file_bytes)

        _, extension = os.path.splitext(filename)
        if extension == '.pdf':
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(filename)
        elif extension == '.docx':
            from langchain_community.document_loaders import Docx2txtLoader
            loader = Docx2txtLoader(filename)
        elif extension == '.txt':
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(filename)
        else:
            st.write("Document format is not supported!")

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200, chunk_overlap=40,
        )
        chunks = text_splitter.split_documents(documents)

        embedding_model = "nomic-embed-text"
        ollama.pull(embedding_model)
        embeddings = OllamaEmbeddings(model=embedding_model)
        vector_store = Chroma.from_documents(chunks, embeddings)

        # st.write(chunks[0])
        # st.write(chunks[1])

        # a simple technique to generate multiple questions from a single question
        # and then retrieve documents based on those questions, getting
        # the best of both worlds.

        chat_model = ChatOllama(model="llama3.2")
        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is to generate five different versions of the given user question to retrieve relevant documents from a vector database. By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Provide these alternative questions separated by newlines.
            Original question: {question}""",  # noqa
        )
        retriever = MultiQueryRetriever.from_llm(
            vector_store.as_retriever(), chat_model, prompt=QUERY_PROMPT
        )

        # RAG prompt

        template = """Answer the question based ONLY on the following context:
        {context}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | chat_model
            | StrOutputParser()
        )
        st.session_state.chain = chain
        st.success("File uploaded, chuncked and embedded successfully")


question = st.text_input("Input your question")
if question:
    if "chain" in st.session_state:
        chain = st.session_state.chain
        res = chain.invoke(input=(question))
        st.write(res)
