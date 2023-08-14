import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx
import csv
from io import StringIO
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def get_webpage_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join([paragraph.get_text() for paragraph in paragraphs])
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from URL: {e}")
        return ""

def get_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        urls = [url.text for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        return urls
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching sitemap: {e}")
        return []

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_file_text(files):
    text = ""
    for file in files:
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == 'pdf':
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file_extension == 'docx':
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_extension == 'txt':
            text += file.getvalue().decode("utf-8") + "\n"
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):   
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):   
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def main():
    
    load_dotenv()
    st.set_page_config(page_title="Chat with Own Documents", page_icon=":books:")
    

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history here
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask a question about your documents:"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            if st.session_state.conversation:
                response = st.session_state.conversation({'question': prompt})
                full_response = response['answer']  # Extract the response text
                st.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            else:
                st.error("Please process documents first.")
            
    with st.sidebar:
        st.subheader("Select data source")
       # data_source = st.radio("Choose data source:", ("Uploaded Files", "Website URLs","Combined" ,"Sitemap URLs"))
        data_source = st.radio("Choose data source:", ("Uploaded Files", "Website URLs", ))
        if data_source == "Uploaded Files":
            uploaded_files = st.file_uploader(
                "Upload your PDF, Txt, Doc files here and click on 'Process'", accept_multiple_files=True)
            if st.button("Process"):
                with st.spinner("Processing"):
                    raw_text = get_file_text(uploaded_files)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(
                        vectorstore)
        elif data_source == "Website URLs":
            urls = st.text_area("Enter website URLs (one per line):")
            url_list = urls.split("\n")
            if st.button("Process"):
                with st.spinner("Processing"):
                    all_text = ""
                    for url in url_list:
                        raw_text = get_webpage_text(url)
                        all_text += raw_text + "\n\n"
                    text_chunks = get_text_chunks(all_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
        elif data_source == "Sitemap URLs":
            sitemap_url = st.text_input("Enter the URL of the sitemap.xml:")
            if st.button("Process"):
                with st.spinner("Processing"):
                    urls_from_sitemap = get_urls_from_sitemap(sitemap_url)
                    all_text = ""
                    for url in urls_from_sitemap:
                        raw_text = get_webpage_text(url)
                        all_text += raw_text + "\n\n"
                    text_chunks = get_text_chunks(all_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
        elif data_source == "Combined":
            uploaded_files = st.file_uploader(
                "Upload your PDF, Txt, Doc files here", accept_multiple_files=True)
            urls = st.text_area("Enter website URLs (one per line):")
            sitemap_url = st.text_input("Enter the URL of the sitemap.xml:")
            if st.button("Process"):
                with st.spinner("Processing"):
                    all_text = ""
                    # Process uploaded files
                    for uploaded_file in uploaded_files:
                        # Process each uploaded file here
                        pass
                    # Process website URLs
                    url_list = urls.split("\n")
                    for url in url_list:
                        raw_text = get_webpage_text(url)
                        all_text += raw_text + "\n\n"
                    # Process sitemap URLs
                    urls_from_sitemap = get_urls_from_sitemap(sitemap_url)
                    for url in urls_from_sitemap:
                        raw_text = get_webpage_text(url)
                        all_text += raw_text + "\n\n"
                    text_chunks = get_text_chunks(all_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()
