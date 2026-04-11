# ---------------- BLOG GENERATION PROMPT ----------------
def blog_prompt(title, keywords, words, tone, context):

    return f"""
You are an expert AI blog writer.

Use the following research context to ensure factual accuracy:
{context}

Write a high-quality blog with the following details:

Title: {title}
Keywords: {keywords}
Word Count: approximately {words}
Tone: {tone}

Instructions:
- Start with an engaging introduction
- Include real insights and statistics if available
- Use proper headings and structure
- Naturally incorporate keywords for SEO
- Add examples where possible
- End with a strong conclusion

Make the blog informative, engaging, and SEO-optimized.
"""


# ---------------- SUMMARY PROMPT ----------------
def summary_prompt(blog):

    return f"""
Analyze the following blog and extract 5 key insights:

{blog}

Return concise bullet points.
"""


# ---------------- QUOTES PROMPT ----------------
def quotes_prompt(topic):

    return f"""
Provide 3 expert-level quotes related to the topic: "{topic}"

Format:
"Quote" — Author
"""


# ---------------- SEO ANALYSIS PROMPT (ADVANCED) ----------------
def seo_prompt(blog, keywords):

    return f"""
Analyze the SEO quality of the following blog.

Blog:
{blog}

Keywords:
{keywords}

Evaluate:
- Keyword usage
- Readability
- Structure
- Engagement

Give a score out of 100 and suggestions for improvement.
"""


# ---------------- FACT CHECK PROMPT (OPTIONAL PRO FEATURE) ----------------
def fact_check_prompt(blog):

    return f"""
Check the following blog for factual correctness.

Identify:
- Any incorrect statements
- Any hallucinated content

Blog:
{blog}

Return a brief analysis.
"""