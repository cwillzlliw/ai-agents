import streamlit as st
from groq import Groq
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)

def run_agent(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a compliance analyst for small healthcare practices. Search the web when needed. Always cite sources."
            },
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def summarize_document(content):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a compliance analyst for small healthcare practices. "
                    "When given a document produce: "
                    "1) A 3-sentence summary, "
                    "2) Key points as a bullet list, "
                    "3) Any compliance gaps or risks you notice."
                )
            },
            {
                "role": "user",
                "content": f"Please analyze this document:\n\n{content}"
            }
        ]
    )
    return response.choices[0].message.content

# ── UI ──────────────────────────────────────────────────
st.title("Kingswill Compliance Assistant")
st.caption("Powered by AI — for small healthcare and therapy practices")

tab1, tab2 = st.tabs(["Ask a Question", "Analyze a Document"])

# Tab 1 — Q&A Agent
with tab1:
    st.subheader("Ask a Compliance Question")
    question = st.text_input("Enter your question:")
    if st.button("Get Answer", key="qa"):
        if question:
            with st.spinner("Researching..."):
                answer = run_agent(question)
            st.markdown(answer)
        else:
            st.warning("Please enter a question.")

# Tab 2 — Document Summarizer
with tab2:
    st.subheader("Analyze a Policy Document")
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if st.button("Analyze Document", key="doc"):
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            with st.spinner("Analyzing..."):
                result = summarize_document(content)
            st.markdown(result)
        else:
            st.warning("Please upload a file first.")