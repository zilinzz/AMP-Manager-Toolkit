# loaders.py
# from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import PyPDFLoader
import os


def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            documents.extend(docs)
    return documents


docs = load_documents('data')


# print(docs)  


# splitters.py
from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(documents)
    return docs


split_docs = split_documents(docs)
# print(split_documents(docs))




# embeddings.py
from langchain.embeddings import OpenAIEmbeddings
import os


def get_embeddings():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    return embeddings


embeddings = get_embeddings()




# vector_store.py
from langchain.vectorstores import FAISS  # or use Chroma
# from embeddings import get_embeddings


# Create the embeddings object
embeddings = OpenAIEmbeddings()


def create_vector_store(documents):
    # Use the embeddings object directly, no need for get_embeddings
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local("vectorstore")
    return vector_store


# Assuming 'split_docs' is your list of document texts
vector_store = create_vector_store(split_docs)


print(vector_store.embeddings.shape)  # (num_documents, embedding_size)
