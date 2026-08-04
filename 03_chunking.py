"""
03_chunking.py
---------------
تقسيم المستندات المُنظّفة إلى أجزاء (chunks) صغيرة مناسبة للـ embedding والبحث.

الموديول المستخدم:
- langchain_text_splitters.RecursiveCharacterTextSplitter
"""

import importlib.util

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def _load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chunk_documents(docs: list, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """يقسم قائمة Document إلى أجزاء أصغر (chunks) باستخدام RecursiveCharacterTextSplitter."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", ".", "،", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ تم تقسيم النص إلى {len(chunks)} جزء (Chunk).")
    return chunks


if __name__ == "__main__":
    documents_module = _load_module("01_documents.py", "documents_module")
    preprocessing_module = _load_module("02_preprocessing.py", "preprocessing_module")

    docs = documents_module.load_documents()
    docs = preprocessing_module.clean_documents(docs)
    chunks = chunk_documents(docs)

    if chunks:
        print("\nمثال على أول Chunk:")
        print(chunks[0].page_content[:300])
