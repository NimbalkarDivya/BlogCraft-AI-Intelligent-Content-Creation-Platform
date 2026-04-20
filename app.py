import streamlit as st
import time
import os

# 🔑 Load environment variables
from dotenv import load_dotenv
load_dotenv()

# 🔥 Groq LLM
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile")

# ---------------- SAFE GENERATE FUNCTION ----------------
def safe_generate(prompt):
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ---------------- RAG IMPORTS ----------------
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ---------------- EMBEDDING MODEL ----------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- VECTOR STORE ----------------
dimension = 384
index = faiss.IndexFlatL2(dimension)
documents = []

# ---------------- LOAD DOCUMENTS ----------------
def load_docs():
    folder = "data/docs"
    texts = []

    if not os.path.exists(folder):
        os.makedirs(folder)

    for file in os.listdir(folder):
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            texts.append(f.read())

    return texts

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def prepare_rag():
    docs = load_docs()
    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)

    embeddings = [embed_model.encode(chunk) for chunk in all_chunks]

    if len(embeddings) > 0:
        index.add(np.array(embeddings))
        documents.extend(all_chunks)

def retrieve_context(query, k=3):
    if len(documents) == 0:
        return ""

    query_embedding = embed_model.encode(query)
    D, I = index.search(np.array([query_embedding]), k)

    return "\n".join([documents[i] for i in I[0]])

# Load RAG once
if "rag_loaded" not in st.session_state:
    prepare_rag()
    st.session_state.rag_loaded = True

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="BlogCraft AI PRO",
    page_icon="✍️",
    layout="wide"
)

# ---------------- MEMORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ----------------
st.title("🚀 BlogCraft AI")
st.subheader("RAG-powered Intelligent Blog Writing Assistant")

st.markdown("""
Generate **high-quality, research-backed blogs** using AI + RAG.

### 🔥 Features:
- AI Blog Writer (Context-Aware)
- Research Retrieval (RAG)
- Expert Quotes
- SEO Analysis
- Memory Tracking
""")

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("⚙️ Blog Settings")

    blog_title = st.text_input("Blog Title")
    keywords = st.text_area("Keywords (comma separated)")
    num_words = st.slider("Blog Length", 300, 1500, step=200)

    tone = st.selectbox(
        "Writing Style",
        ["Professional", "Educational", "Technical", "Storytelling"]
    )

    generate_btn = st.button("🚀 Generate Blog")

# ---------------- BLOG GENERATOR ----------------
def generate_blog(title, keywords, words, tone):

    context = retrieve_context(title + " " + keywords)

    prompt = f"""
You are an expert blog writer.

Use the following research context:
{context}

Write a well researched blog.

Title: {title}
Keywords: {keywords}
Word Count: approximately {words}
Tone: {tone}

Include:
- Introduction
- Research insights
- Statistics
- Expert quotes
- SEO optimization
- Conclusion
"""

    return safe_generate(prompt)

# ---------------- SUMMARY ----------------
def generate_summary(blog):
    prompt = f"Summarize into 5 key insights:\n{blog}"
    return safe_generate(prompt)

# ---------------- QUOTES ----------------
def generate_quotes(topic):
    prompt = f'Give 3 expert quotes on "{topic}"'
    return safe_generate(prompt)

# ---------------- SEO ----------------
def seo_score(blog, keywords):
    return sum([blog.lower().count(k.strip()) for k in keywords.split(",")])

# ---------------- MAIN ----------------
if generate_btn:

    if blog_title.strip() == "" or keywords.strip() == "":
        st.warning("⚠️ Please enter blog title and keywords")

    else:

        with st.spinner("Generating AI blog with RAG..."):
            time.sleep(1)

            blog = generate_blog(blog_title, keywords, num_words, tone)

            if "⚠️" in blog:
                st.error(blog)
                st.stop()

            summary = generate_summary(blog)
            quotes = generate_quotes(blog_title)
            score = seo_score(blog, keywords)

            # Save history
            st.session_state.history.append({
                "title": blog_title,
                "blog": blog
            })

        st.success("✅ Blog Generated")

        col1, col2 = st.columns([2, 1])

        # -------- BLOG --------
        with col1:
            st.header("📄 Blog Content")
            st.markdown(blog)

        # -------- INSIGHTS --------
        with col2:
            st.header("📊 Insights")

            st.subheader("Key Takeaways")
            st.markdown(summary)

            st.subheader("Expert Quotes")
            st.markdown(quotes)

            st.subheader("SEO Score")
            st.metric("Score", score)

        # -------- ANALYTICS --------
        st.divider()

        col3, col4, col5 = st.columns(3)

        with col3:
            st.metric("Target Words", num_words)

        with col4:
            st.metric("Keywords", len(keywords.split(",")))

        with col5:
            st.metric("Reading Time", f"{int(num_words/200)} min")

        # -------- DOWNLOAD --------
        st.download_button(
            label="⬇ Download Blog",
            data=blog,
            file_name="blogcraft_article.txt",
            mime="text/plain"
        )

# ---------------- HISTORY ----------------
st.sidebar.divider()
st.sidebar.subheader("🕓 History")

for item in st.session_state.history[-5:]:
    st.sidebar.write(f"• {item['title']}")