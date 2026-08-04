# مساعد خدمة العملاء - RAG Project

مشروع RAG بسيط للرد على استفسارات العملاء بالاعتماد فقط على مستندات PDF الخاصة بالشركة،
باستخدام Gemini (Google) + Chroma + HuggingFace Embeddings.

## المسار (Pipeline)
```
01_documents.py            -> تحميل ملفات PDF
02_preprocessing.py        -> تنظيف النص
03_chunking.py              -> تقسيم النص لأجزاء
04_vector_representation.py -> تحويل الأجزاء لمتجهات (embeddings)
05_create_chroma_store.py  -> بناء/حفظ قاعدة بيانات Chroma
06_retrieve_context.py     -> استرجاع السياق الأنسب للسؤال
07_prompting.py             -> بناء البرومبت واستدعاء موديل Gemini
streamlit_app.py            -> واجهة المستخدم
```

## التشغيل محلياً

1. ثبّت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```

2. أنشئ ملف البيئة المحلي من القالب:
   - على Windows PowerShell:
     ```powershell
     copy .env.example .env
     ```
   - على macOS/Linux:
     ```bash
     cp .env.example .env
     ```
   ثم عدّل ملف `.env` وأدخل مفتاح Google API الحقيقي.

3. ضع ملفات PDF الخاصة بك داخل مجلد `data/`.

4. بنِ قاعدة البيانات (مرة واحدة، أو كل ما تغيرت الملفات):
   ```bash
   python 05_create_chroma_store.py
   ```

5. شغّل التطبيق:
   ```bash
   streamlit run streamlit_app.py
   ```

## النشر على GitHub وStreamlit Cloud

1. ارفع المشروع على GitHub مع إبعاد الملفات الحساسة:
   - `.env`
   - `chroma_db/`
   - `.streamlit/secrets.toml`
   
   هذه العناصر موجودة بالفعل في `.gitignore`.

2. لأن `chroma_db/` غالباً كبير جداً لرفعه على GitHub، أفضل حل هو تشغيل
   `05_create_chroma_store.py` مرة واحدة أونلاين (مثلاً في Colab أو جهاز آخر)
   ثم رفع مجلد `chroma_db/` الناتج لاحقاً إن لزم الأمر.

3. على Streamlit Cloud: افتح Manage app -> Secrets وأضف القيم التالية بصيغة TOML
   باستخدام مثال الملف `secrets.toml.example`:
   ```toml
   OPENROUTER_API_KEY = "مفتاحك الحقيقي هنا"
   OPENROUTER_MODEL = "openrouter/free"
   ```

4. شغّل التطبيق من Streamlit Cloud.

## ⚠️ تنبيه أمان
- لا تكتب المفتاح الحقيقي داخل أي ملف بايثون.
- لا ترفع ملف `.env` الحقيقي أو `chroma_db/` على GitHub.
- لو سبق ونشرت مفتاح API حقيقي في أي مكان (شات، كود، الخ) قم بإلغائه (revoke)
  فوراً من لوحة تحكم OpenRouter (openrouter.ai/keys) وأنشئ مفتاحاً جديداً.
