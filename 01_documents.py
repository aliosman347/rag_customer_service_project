"""
01_documents.py
----------------
مسؤول عن قراءة ملفات PDF الخام من مجلد المصدر وتحويلها إلى Document objects
باستخدام LangChain.

الموديول المستخدم:
- langchain_community.document_loaders.PyPDFDirectoryLoader
"""

import os
from langchain_community.document_loaders import PyPDFDirectoryLoader

# مسار مجلد ملفات PDF (يمكن تغييره أو تمريره كمتغير بيئة)
DEFAULT_PDF_FOLDER = os.environ.get("PDF_FOLDER", "data")


def load_documents(folder_path: str = DEFAULT_PDF_FOLDER):
    """
    يقرأ كل ملفات PDF الموجودة داخل folder_path ويرجع قائمة Document.
    """
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(
            f"❌ المجلد '{folder_path}' غير موجود. ضع ملفات PDF بداخله أولاً."
        )

    loader = PyPDFDirectoryLoader(folder_path)
    docs = loader.load()

    if not docs:
        print(f"⚠️ لم يتم العثور على أي ملفات PDF داخل '{folder_path}'.")
    else:
        print(f"✅ تم تحميل {len(docs)} صفحة من المجلد '{folder_path}'.")

    return docs


if __name__ == "__main__":
    documents = load_documents()
    if documents:
        print("\nمثال من أول صفحة:")
        print(documents[0].page_content[:300])
