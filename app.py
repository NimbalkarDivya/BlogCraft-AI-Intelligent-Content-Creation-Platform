import streamlit as st
from google import genai
import time

# ---------------- API KEY ----------------
API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

# Model (supported Gemini model)
MODEL = "gemini-1.5-flash"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="BlogCraft AI",
    page_icon="✍️",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("✍️ BlogCraft AI")
st.subheader("Intelligent Automated Blog Writing Assistant")

st.markdown("""
Generate **high-quality research-based blogs** using AI.

Features:
- AI Blog Writer
- Research Insights
- Expert Quotes
- SEO Keywords Analysis
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

    prompt = f"""
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
- Conclusion
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


# ---------------- SUMMARY ----------------
def generate_summary(blog):

    prompt = f"""
Summarize this blog into 5 key research insights:

{blog}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


# ---------------- QUOTES ----------------
def generate_quotes(topic):

    prompt = f"""
Give 3 expert quotes related to {topic}.

Format:
"Quote" — Author
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


# ---------------- MAIN GENERATION ----------------
if generate_btn:

    if blog_title.strip() == "" or keywords.strip() == "":
        st.warning("⚠️ Please enter blog title and keywords")

    else:

        with st.spinner("Generating AI blog..."):
            time.sleep(1)

            blog = generate_blog(blog_title, keywords, num_words, tone)

        st.success("✅ Blog Generated")

        col1, col2 = st.columns([2,1])

        # -------- BLOG CONTENT --------
        with col1:

            st.header("📄 Blog Content")

            st.markdown(blog)

        # -------- BLOG INSIGHTS --------
        with col2:

            st.header("📊 Blog Insights")

            summary = generate_summary(blog)

            st.subheader("Key Takeaways")

            st.markdown(summary)

            st.subheader("Expert Quotes")

            quotes = generate_quotes(blog_title)

            st.markdown(quotes)

        # -------- BLOG ANALYTICS --------
        st.divider()

        col3, col4, col5 = st.columns(3)

        with col3:
            st.metric("Target Word Count", num_words)

        with col4:
            keyword_count = len(keywords.split(","))
            st.metric("Keywords", keyword_count)

        with col5:
            reading_time = int(num_words / 200)
            st.metric("Reading Time", f"{reading_time} min")

        # -------- DOWNLOAD BLOG --------
        st.download_button(
            label="⬇ Download Blog",
            data=blog,
            file_name="blogcraft_article.txt",
            mime="text/plain"
        )