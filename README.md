# 🚀 BlogCraft AI - Intelligent Content Creation Platform

## 🧠 Overview
BlogCraft AI is a RAG-powered AI blog generation system that creates high-quality, SEO-optimized blogs using Gemini API and contextual knowledge retrieval.

## 🔥 Features
- 🧠 RAG-based blog generation (context-aware)
- ✍️ AI blog writer with structured output
- 📊 Blog insights (summary + quotes)
- 🔍 SEO keyword analysis
- 🧠 Session memory tracking

## ⚙️ Tech Stack
- Python
- Streamlit
- Google Gemini API
- FAISS (Vector Database)
- Sentence Transformers

## 🏗️ Architecture
User Input → RAG Retrieval → Prompt Engineering → Gemini LLM → Blog Output

## 📁 Project Structure
BlogCraft/
│── app.py
│── rag/
│── utils/
│── data/docs/
│── requirements.txt

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py