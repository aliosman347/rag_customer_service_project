import importlib.util
import os
import subprocess
import sys
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="مساعد خدمة العملاء", page_icon="🤖")


def _load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


retrieve_module = _load_module("06_retrieve_context.py", "retrieve_module")
prompting_module = _load_module("07_prompting.py", "prompting_module")

try:
    if not getattr(prompting_module, "OPENROUTER_API_KEY", None):
        prompting_module.OPENROUTER_API_KEY = st.secrets.get(
            "OPENROUTER_API_KEY", ""
        )
        prompting_module.OPENROUTER_MODEL = st.secrets.get(
            "OPENROUTER_MODEL", "openrouter/free"
        )
except Exception:
    pass

st.title("🤖 مساعد خدمة العملاء (RAG)")
st.caption(
    "اسأل أي سؤال عن خدماتنا، والإجابة هتكون مبنية على المستندات المتاحة فقط."
)


@st.cache_resource(show_spinner="⏳ جاري تحميل/بناء قاعدة البيانات...")
def get_retriever():
    if not os.path.exists("chroma_db"):
        st.info("⚙️ جاري إنشاء قاعدة البيانات لأول مرة...")
        # تشغيل السكريبت وطباعة أي خطأ بالتفصيل لو حصل
        result = subprocess.run(
            [sys.executable, "05_create_chroma_store.py"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            st.error("❌ فشل إنشاء قاعدة البيانات!")
            st.code(result.stderr, language="bash")
            st.stop()

    vectordb = retrieve_module.load_vectorstore()
    return retrieve_module.get_retriever(vectordb)


@st.cache_resource(show_spinner="⏳ جاري تحميل الموديل...")
def get_llm():
    return prompting_module.get_llm(
        api_key=prompting_module.OPENROUTER_API_KEY,
        model_name=prompting_module.OPENROUTER_MODEL,
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("اكتب استفسارك هنا...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        try:
            retriever = get_retriever()
            llm = get_llm()
            result = prompting_module.answer_question(
                user_question, retriever, llm
            )

            answer = result["answer"]
            sources = result["sources"]

            st.markdown(answer)

            if sources:
                with st.expander("📚 المصادر"):
                    for s in sources:
                        st.markdown(
                            f"- **{s['source']}** (صفحة {s['page']})"
                        )

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            error_msg = f"حدث خطأ: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_msg}
            )