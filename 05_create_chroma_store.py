"""
05_create_chroma_store.py
---------------------------
السكريبت الرئيسي لبناء قاعدة بيانات Chroma:
documents -> preprocessing -> chunking -> vector representation -> vector store

شغّل هذا الملف مرة واحدة (أو كل ما تحدّث ملفات PDF) لبناء/تحديث قاعدة البيانات:
    python 05_create_chroma_store.py

الموديول المستخدم:
- langchain_chroma.Chroma
"""

import os
import importlib.util
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

CHROMA_DIR = os.environ.get("CHROMA_DIR", "chroma_db")


def _load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_vectorstore(persist_directory: str = CHROMA_DIR):
    from langchain_chroma import Chroma

    documents_module = _load_module("01_documents.py", "documents_module")
    preprocessing_module = _load_module("02_preprocessing.py", "preprocessing_module")
    chunking_module = _load_module("03_chunking.py", "chunking_module")
    vector_module = _load_module("04_vector_representation.py", "vector_module")

    # 1) تحميل المستندات
    docs = documents_module.load_documents()

    # 2) التنظيف
    docs = preprocessing_module.clean_documents(docs)

    # 3) التقسيم
    chunks = chunking_module.chunk_documents(docs)

    # 4) موديل الـ embeddings
    embeddings = vector_module.get_embedding_model()

    # 5) بناء قاعدة بيانات Chroma وحفظها على القرص
    print(f"⏳ بناء قاعدة بيانات Chroma في '{persist_directory}' ...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    print("✅ تم بناء قاعدة البيانات وحفظها بنجاح.")
    return vectordb


if __name__ == "__main__":
    build_vectorstore()
