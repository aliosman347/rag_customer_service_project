"""
04_vector_representation.py
-----------------------------
تحويل الأجزاء (chunks) إلى تمثيل متجهي (vectors) باستخدام موديل embeddings
متعدد اللغات (يدعم العربي والإنجليزي).

الموديول المستخدم:
- langchain_huggingface.HuggingFaceEmbeddings
- موديل: intfloat/multilingual-e5-small
"""

EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-small"


def get_embedding_model(model_name: str = EMBEDDING_MODEL_NAME):
    """يرجع موديل embeddings جاهز للاستخدام مع Chroma."""
    from langchain_huggingface import HuggingFaceEmbeddings

    print(f"⏳ تحميل موديل الـ embeddings: {model_name} ...")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    print("✅ تم تحميل موديل الـ embeddings بنجاح.")
    return embeddings


if __name__ == "__main__":
    model = get_embedding_model()
    sample_vector = model.embed_query("مرحباً بك في خدمة العملاء")
    print(f"طول المتجه الناتج: {len(sample_vector)}")
