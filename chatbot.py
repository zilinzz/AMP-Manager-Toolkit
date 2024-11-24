# Import necessary modules
import os
from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_community.vectorstores import FAISS  # or Chroma
from langchain_community.document_loaders import GoogleDriveLoader
from flask import Flask, request, jsonify
from flask_cors import CORS


# Load environment variables
load_dotenv()


# Step 1: Load Documents
# directory = 'data'
# documents = []
# for filename in os.listdir(directory):
#     if filename.endswith('.pdf'):
#         filepath = os.path.join(directory, filename)
#         loader = PyPDFLoader(filepath)
#         docs = loader.load()
#         documents.extend(docs)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route('/')
def home():
    return "Welcome to the QA chatbot server!"

# Step 1: Load Documents - google drive
credentials_path = "credentials.json"
loader = GoogleDriveLoader(document_ids=["1qDZrBNQuNhIl11RaFmbLws9UX43SVTFH-sK70Lun2bU"],
                          credentials_path=credentials_path)
docs = loader.load()



# Step 2: Split Documents
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200,
# )
# split_docs = text_splitter.split_documents(documents)

# Step 3: Get Embeddings
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables.")

# # Print part of the API key for debugging purposes
# print(f"Using OpenAI API key: {openai_api_key[:8]}****")

# Create the embeddings object
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Step 4: Create & Save Vector Store
vector_store = FAISS.from_documents(docs, embeddings)
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

qa_chain = create_qa_chain()

# Example usage
# if __name__ == "__main__":

    # Example question to ask the QA chain
    # question = "Can you give me the link to change management toolkit?"
    # question = "What are the two roles that the Change Management Toolkit is designed to support?"
    # question = "What office organizes business process improvement at UC Berkeley?"
    # question = "What services does the Business Process Management office provide?"
    # question = "Name two types of resources available under the Project Management Resources section."
    # question = "What are the primary goals of IT change management?"

    # Get the answer from the QA chain
    # answer = qa_chain.invoke({"query": question})
    
    # print(f"Answer: {answer}")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    try:
        answer = qa_chain.invoke({"query": user_input})
        return jsonify({'response': answer}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


    