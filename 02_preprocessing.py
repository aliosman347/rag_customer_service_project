"""
02_preprocessing.py
--------------------
تنظيف النصوص المستخرجة من PDF (إزالة أسطر جديدة زائدة، مسافات مكررة..).
نفس فكرة "التنظيف السحري" الموجودة في نوتبوكك الأصلي.

الموديول المستخدم:
- re (مكتبة بايثون القياسية)
"""

import re


def clean_text(text: str) -> str:
    """ينظف نص واحد: يحول أسطر جديدة لمسافات ويشيل المسافات المكررة."""
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_documents(docs: list):
    """يطبق clean_text على كل Document في القائمة ويرجع نفس القائمة بعد التنظيف."""
    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    if docs:
        print(f"✅ تم تنظيف {len(docs)} صفحة بنجاح.")
    return docs


if __name__ == "__main__":
    import importlib.util

    spec = importlib.util.spec_from_file_location("documents_module", "01_documents.py")
    documents_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(documents_module)

    docs = documents_module.load_documents()
    cleaned = clean_documents(docs)
    if cleaned:
        print("\nمثال بعد التنظيف:")
        print(cleaned[0].page_content[:300])
