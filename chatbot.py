# Import necessary modules
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_community.vectorstores import FAISS  # or Chroma

# Load environment variables
load_dotenv()

# Step 1: Load Documents
directory = 'data'
documents = []
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        filepath = os.path.join(directory, filename)
        loader = PyPDFLoader(filepath)
        docs = loader.load()
        documents.extend(docs)

# Step 2: Split Documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
split_docs = text_splitter.split_documents(documents)

# Step 3: Get Embeddings
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables.")

# # Print part of the API key for debugging purposes
# print(f"Using OpenAI API key: {openai_api_key[:8]}****")

# Create the embeddings object
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Step 4: Create & Save Vector Store
vector_store = FAISS.from_documents(split_docs, embeddings)
vector_store.save_local("vectorstore")

# Output the number of documents stored
print(f"Number of documents stored in vector store: {vector_store.index.ntotal}")


# Step 5: Set Up the Retrieval Augmented Generation (RAG) Chain
def create_qa_chain():
    # Initialize the language model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

    # Set up the retriever from the vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Set up the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # You can experiment with other chain types like 'map_reduce'
        retriever=retriever,
        return_source_documents=False,  # Set to True if you want to return source documents
    )

    return qa_chain

# Example usage
if __name__ == "__main__":
    qa_chain = create_qa_chain()

    # Example question to ask the QA chain
    question = "What is change management?"
    
    # Get the answer from the QA chain
    answer = qa_chain.invoke({"query": question})
    
    print(f"Answer: {answer}")