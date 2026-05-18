import os
import json
from functools import lru_cache
from pathlib import Path
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")


# ========================
# Chain Factory
# ========================

@lru_cache(maxsize=1)
def get_qa_chain():

    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        raise RuntimeError(
            "MISTRAL_API_KEY is missing. Add it to your .env file before using the assistant."
        )

    try:
        from langchain_mistralai import ChatMistralAI
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            f"Missing RAG dependency: {exc.name}. Install the project requirements in .venv."
        ) from exc

    try:
        from langchain_chroma import Chroma
    except ModuleNotFoundError:
        from langchain_community.vectorstores import Chroma

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ModuleNotFoundError:
        from langchain_community.embeddings import HuggingFaceEmbeddings

    try:
        from langchain_classic.chains import RetrievalQA
    except ModuleNotFoundError:
        from langchain.chains import RetrievalQA

    try:
        embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5"
        )
    except ImportError as exc:
        raise RuntimeError(
            "Missing RAG dependency: sentence-transformers. Install the project requirements in .venv."
        ) from exc

    vectorstore = Chroma(
        persist_directory=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
        embedding_function=embedding_model
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 5
        }
    )

    llm = ChatMistralAI(
        model=os.getenv("MISTRAL_MODEL", "mistral-small"),
        api_key=api_key
    )

    prompt_template = """

    You are a financial AI assistant.

    Use ONLY the provided context to answer.

    If the answer is not found in the context,
    say:

    "I could not find the answer in the knowledge base."

    Do not use external knowledge.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    PROMPT = PromptTemplate(

      template=prompt_template,

      input_variables=[
          "context",
          "question"
      ]
    )

    return RetrievalQA.from_chain_type(

      llm=llm,

      retriever=retriever,

      chain_type_kwargs={
         "prompt": PROMPT
       }
    )

# ========================
# Ask Function
# ========================

def ask_rag(question):

    if not question or not question.strip():

        raise ValueError(
            "Question cannot be empty."
        )

    # =====================================
    # LOAD LAST PREDICTION
    # =====================================

    try:

        with open(
            "data/latest_prediction.json",
            "r"
        ) as f:

            prediction_context = json.load(f)

    except Exception:

        prediction_context = {}

    # =====================================
    # AUGMENTED QUESTION
    # =====================================

    augmented_question = f"""

    User Question:
    {question}

    Client Prediction Context:
    {prediction_context}

    Explain the prediction using
    the underwriting policies
    and financial context.
    """

    # =====================================
    # DEBUG RETRIEVED DOCS
    # =====================================

    docs = (

        get_qa_chain()

        .retriever

        .invoke(augmented_question)
    )

    for i, doc in enumerate(docs):

        print(f"\n--- DOC {i} ---\n")

        print(doc.page_content[:500])

    # =====================================
    # RAG RESPONSE
    # =====================================

    response = (

        get_qa_chain()

        .invoke(augmented_question)
    )

    return response["result"]