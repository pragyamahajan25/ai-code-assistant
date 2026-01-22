import streamlit as st
from rag_helper import ask_rag, create_vectorstore
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from langchain_core.documents import Document

st.set_page_config(page_title="AI Code Assistant", layout="wide")
st.title("AI Code Assistant with RAG")
st.write("Paste your code, ask questions, and get AI explanations grounded in docs or references.")

# Sidebar settings
st.sidebar.header("Settings")
num_suggestions = st.sidebar.slider("Number of suggestions", 1, 5, 1)
code_language = st.sidebar.text_input("Specify language (optional, e.g., python, java)")

# Code input
code_snippet = st.text_area("Enter your code snippet here:", height=300)

# Question input
question = st.text_input("Ask a question about the code:")

def display_code(code, language=None):
    try:
        lexer = get_lexer_by_name(language) if language else guess_lexer(code)
        formatter = HtmlFormatter(style="monokai", full=False, noclasses=True)
        highlighted_code = highlight(code, lexer, formatter)
        st.markdown(highlighted_code, unsafe_allow_html=True)
    except Exception:
        st.code(code)

# Mock documents for RAG
docs = [
    Document(
        page_content="Python lists can be sliced using list[start:end]",
        metadata={"source": "Python Docs"}
    ),
    Document(
        page_content="In Python, use 'with open(filename)' to read files safely",
        metadata={"source": "Python Docs"}
    ),
    Document(
        page_content="Use list comprehensions instead of loops for efficiency",
        metadata={"source": "Python Tips"}
    ),
]

# Build vectorstore once
vectorstore = create_vectorstore(docs)

if st.button("Analyze Code with RAG"):
    if not code_snippet.strip():
        st.warning("Please enter a code snippet.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating response..."):
            answer, sources = ask_rag(
                question,
                code_snippet,
                vectorstore
            )

        st.subheader("Code Snippet:")
        display_code(code_snippet, code_language)

        st.subheader("AI Suggestion / Explanation:")
        st.write(answer)

        if sources:
            st.subheader("Sources Used:")
            for src in sources:
                st.write(f"- {src}")
