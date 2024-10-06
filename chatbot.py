# loaders.py
from langchain.document_loaders import UnstructuredPDFLoader
import os

def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            loader = UnstructuredPDFLoader(filepath)
            docs = loader.load()
            documents.extend(docs)
    return documents

docs = load_documents('data')

print(docs)  

# splitters.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(documents)
    return docs
