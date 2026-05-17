from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)


# =========================================
# PATHS
# =========================================

BASE_DIR = Path(__file__).resolve().parents[3]

DOCS_DIR = BASE_DIR / "docs"

CHROMA_DIR = BASE_DIR / "chroma_db"


# =========================================
# EMBEDDINGS
# =========================================

embedding_model = HuggingFaceEmbeddings(

    model_name=
    "BAAI/bge-base-en-v1.5"
)


# =========================================
# VECTOR STORE
# =========================================

vectorstore = Chroma(

    persist_directory=str(CHROMA_DIR),

    embedding_function=embedding_model
)


# =========================================
# TEXT SPLITTER
# =========================================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=100
)


# =========================================
# LOAD MARKDOWN FILES
# =========================================

all_chunks = []

md_files = list(
    DOCS_DIR.glob("*.md")
)

print(f"Found {len(md_files)} markdown files")


for md_path in md_files:

    print(f"\nLoading: {md_path.name}")

    loader = TextLoader(
        str(md_path),
        encoding="utf-8"
    )

    documents = loader.load()

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"{len(chunks)} chunks created"
    )

    all_chunks.extend(chunks)


# =========================================
# STORE IN CHROMA
# =========================================

print("\nCreating embeddings...")

vectorstore.add_documents(all_chunks)

print("\nDone.")

print(
    f"{len(all_chunks)} chunks stored."
)