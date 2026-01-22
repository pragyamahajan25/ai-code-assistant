# AI Code Assistant with RAG

An AI-powered code assistant that combines **Streamlit**, **LangChain**, and **Retrieval-Augmented Generation (RAG)** to answer questions about your code using contextual references from external documents. Paste your code, ask questions, and get explanations grounded in documentation and tips.  

---

## Features

- **Code Analysis:** Paste code snippets and ask questions about them.  
- **RAG-Powered Answers:** Answers are informed by related documents via FAISS vector search.  
- **Syntax Highlighting:** Code is displayed with syntax highlighting for better readability.  
- **Customizable Suggestions:** Adjust the number of suggestions and optionally specify the programming language.  
- **Sources Referenced:** The assistant shows which documents were used to generate the answer.  

---

## Demo

Code snippet:
numbers = [10, 20, 30, 40, 50, 60]

print(numbers[:3]) 
print(numbers[-2:]) 
print(numbers[::2])



---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/ai-code-assistant.git
cd ai-code-assistant

## Usage

1. **Run the Streamlit app:**

```bash
streamlit run app.py

In the browser:

Paste your code snippet in the text area.
Enter your question about the code.
Click "Analyze Code with RAG".
View AI suggestions and sources used.

## Project Structure

├── app.py            # Streamlit app
├── rag_helper.py     # RAG utilities: vectorstore & AI query
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation

### `rag_helper.py`

- Initializes embeddings and FAISS vector store.  
- **`create_vectorstore(docs)`**: Converts a list of `Document` objects into a FAISS vectorstore.  
- **`ask_rag(question, code_snippet, vectorstore)`**: Uses a LLM to answer questions with context from retrieved documents.  

### `app.py`

- Streamlit frontend for user input.  
- Allows code snippet entry, question input, and displays highlighted code with AI answers.  
- Uses mock documents for RAG, which can be replaced with real documentation.

## Customization

Add more documents: Extend the docs list in app.py with your own content.
Change LLM model: Modify the model parameter in rag_helper.py (currently gpt-4o-mini).
Adjust vector search: Change k in vectorstore.similarity_search(query_text, k=3) to return more or fewer relevant documents.
