"""
07_prompting.py
"""

import os
import importlib.util

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "openrouter/free")

SYSTEM_PROMPT = """
انت مساعد خدمة عملاء لشركة الكترونيات.
استخدم فقط المعلومات الموجودة في النص ادناه.
لو المعلومة غير موجودة قل انك لا تعرف
واقترح التواصل مع الدعم البشري.
طابق لغة المستخدم (عربي او انجليزي).
اجعل الردود قصيرة وواضحة.

{context}
"""


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_llm(api_key=None, model_name=None):
    from langchain_openai import ChatOpenAI

    api_key = api_key or OPENROUTER_API_KEY
    model_name = model_name or OPENROUTER_MODEL

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY missing. Put it in .env or Streamlit Secrets.")

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2,
    )


def build_prompt():
    from langchain_core.prompts import ChatPromptTemplate

    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ]
    )


def _extract_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts).strip()

    return str(content)


def answer_question(question, retriever, llm=None):
    retrieve_module = _load_module("06_retrieve_context.py", "retrieve_module")

    context, sources = retrieve_module.retrieve_context(retriever, question)

    prompt = build_prompt()
    llm = llm or get_llm()

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})

    return {
        "answer": _extract_text(response.content),
        "sources": sources,
    }


if __name__ == "__main__":
    retrieve_module = _load_module("06_retrieve_context.py", "retrieve_module")

    vectordb = retrieve_module.load_vectorstore()
    retriever = retrieve_module.get_retriever(vectordb)

    result = answer_question("test", retriever)
    print(result["answer"])
    print(result["sources"])
