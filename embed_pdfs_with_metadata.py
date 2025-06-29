import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma  # Updated import
from langchain_openai import OpenAIEmbeddings

# ✅ Load environment variables
load_dotenv()

# ✅ Define your OpenAI API key directly here or use os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = ""

# Function to load and chunk PDF documents with metadata
def load_and_split_with_metadata(folder_path="."):
    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            print(f"📄 Loading: {file}")
            try:
                loader = PyPDFLoader(file_path)
                pages = loader.load_and_split()

                for page in pages:
                    page.metadata["source"] = file

                chunks = splitter.split_documents(pages)
                print(f"📚 {len(chunks)} chunks created from {file}")
                docs.extend(chunks)
            except Exception as e:
                print(f"❌ Failed to load {file}: {e}")

    print(f"✅ Total chunks collected: {len(docs)}")
    return docs

# Function to build vector store and persist
def build_vector_store(docs, persist_directory="chroma_store"):
    if not docs:
        print("⚠️ No documents to embed.")
        return

    print("🧠 Embedding documents...")
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=OPENAI_API_KEY
    )
    vectordb = Chroma.from_documents(documents=docs, embedding=embedding_model, persist_directory=persist_directory)
    vectordb.persist()
    print(f"✅ Vector store saved at: {persist_directory}")

# Main execution
if __name__ == "__main__":
    print("🚀 Starting document embedding pipeline...")
    docs = load_and_split_with_metadata(".")
    build_vector_store(docs)
