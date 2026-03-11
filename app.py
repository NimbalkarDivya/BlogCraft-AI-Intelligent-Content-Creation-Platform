import streamlit as st
from google import genai
import time

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ Gemini API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Gemini model
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


# ---------------- GEMINI CALL FUNCTION ----------------
def call_gemini(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        # Handle Gemini response safely
        if hasattr(response, "text") and response.text:
            return response.text
        else:
            return "⚠️ AI returned an empty response."

    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"


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

    return call_gemini(prompt)


# ---------------- SUMMARY ----------------
def generate_summary(blog):

    prompt = f"""
Summarize this blog into 5 key research insights:

{blog}
"""

    return call_gemini(prompt)


# ---------------- QUOTES ----------------
def generate_quotes(topic):

    prompt = f"""
Give 3 expert quotes related to {topic}.

Format:
"Quote" — Author
"""

    return call_gemini(prompt)


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

        with col1:
            st.header("📄 Blog Content")
            st.markdown(blog)

        with col2:
            st.header("📊 Blog Insights")

            summary = generate_summary(blog)
            st.subheader("Key Takeaways")
            st.markdown(summary)

            quotes = generate_quotes(blog_title)
            st.subheader("Expert Quotes")
            st.markdown(quotes)

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

        st.download_button(
            label="⬇ Download Blog",
            data=blog,
            file_name="blogcraft_article.txt",
            mime="text/plain"
        )