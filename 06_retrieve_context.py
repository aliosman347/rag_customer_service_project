"""
06_retrieve_context.py
------------------------
تحميل قاعدة بيانات Chroma الموجودة على القرص، وإنشاء retriever،
واسترجاع أكثر الأجزاء (chunks) صلة بسؤال المستخدم — مع الاحتفاظ
بمصدر كل جزء (اسم الملف/الصفحة) لأجل الاستشهاد بالمصدر لاحقاً.

الموديول المستخدم:
- langchain_chroma.Chroma
"""

import os
import importlib.util

CHROMA_DIR = os.environ.get("CHROMA_DIR", "chroma_db")
TOP_K = 5


def _load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_vectorstore(persist_directory: str = CHROMA_DIR):
    from langchain_chroma import Chroma

    vector_module = _load_module("04_vector_representation.py", "vector_module")
    embeddings = vector_module.get_embedding_model()

    if not os.path.isdir(persist_directory):
        raise FileNotFoundError(
            f"❌ لم يتم العثور على قاعدة بيانات في '{persist_directory}'. "
            "شغّل 05_create_chroma_store.py أولاً."
        )

    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
    return vectordb


def get_retriever(vectordb, k: int = TOP_K):
    return vectordb.as_retriever(search_type="similarity", search_kwargs={"k": k})


def retrieve_context(retriever, question: str):
    """
    يرجع tuple: (النص المدمج للسياق, قائمة المصادر لكل جزء).
    كل مصدر عبارة عن dict فيه اسم الملف ورقم الصفحة (لو متوفر).
    """
    retrieved_docs = retriever.invoke(question)

    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    sources = []
    for doc in retrieved_docs:
        raw_source = doc.metadata.get("source")
        if raw_source:
            source_name = os.path.basename(raw_source)
        else:
            source_name = "غير معروف"

        page = doc.metadata.get("page")
        if page in (None, ""):
            page = "?"
        else:
            # بعض اللوادر تبدأ ترقيم الصفحات من صفر
            try:
                page = int(page) + 1
            except (TypeError, ValueError):
                pass

        sources.append({"source": source_name, "page": page})

    return context_text, sources


if __name__ == "__main__":
    vectordb = load_vectorstore()
    retriever = get_retriever(vectordb)

    question = "طرق التواصل مع خدمة العملاء"
    context, sources = retrieve_context(retriever, question)

    print(f"=== السياق المسترجع للسؤال: '{question}' ===\n")
    print(context[:500])
    print("\n=== المصادر ===")
    for s in sources:
        print(s)
