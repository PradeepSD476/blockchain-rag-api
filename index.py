import os
import sys
import time
from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import shutil

MANUAL_DOCS_PATH = "./manual_docs" 
VECTOR_DB_PATH = "./vector_db_manual" 

if "GOOGLE_API_KEY" not in os.environ:
    sys.exit(1)

if not os.path.exists(MANUAL_DOCS_PATH) or not os.listdir(MANUAL_DOCS_PATH):
     sys.exit(1)

if os.path.exists(VECTOR_DB_PATH):
    try:
        shutil.rmtree(VECTOR_DB_PATH)
    except Exception as e:
        sys.exit(1)
try:
    loader = DirectoryLoader(
        MANUAL_DOCS_PATH,
        glob="**/*.md",
        loader_cls=UnstructuredMarkdownLoader,
        show_progress=True,
        use_multithreading=True,
        silent_errors=True,
    )
    all_docs = loader.load()
    for doc in all_docs:
        doc.metadata["source"] = doc.metadata.get("source", "unknown").replace(os.getcwd(), ".")
        doc.metadata["framework"] = "manual_hardhat3" 
except Exception as e:
    sys.exit(1)

if not all_docs:
    sys.exit(1)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", "", "##", "#", "###"]
)
chunks = text_splitter.split_documents(all_docs)
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


except Exception as e:
    sys.exit(1)

start_time = time.time()

try:
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH # Save to this folder
    )
    end_time = time.time()

except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)