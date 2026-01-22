from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough


# Initialize embedding model

embedding_model = OpenAIEmbeddings()


def create_vectorstore(docs):
    """
    Create a FAISS vector store from a list of Document objects.
    Each doc is a langchain Document: Document(page_content="text", metadata={})
    """
    return FAISS.from_documents(docs, embedding_model)


def ask_rag(question, code_snippet, vectorstore):
    """
    Ask a question with retrieval-augmented context.
    Returns answer and sources.
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )

    prompt = PromptTemplate.from_template(
        """
You are an AI assistant helping with code.
You have access to external documentation.

Context:
{context}

User Question:
{question}

Code Snippet:
{code_snippet}

Answer clearly and concisely, referring to the context if needed.
"""
    )

    # Combine question + code snippet for retrieval
    query_text = f"{question}\n\nCode:\n{code_snippet}"

    # Direct FAISS search (safe for all versions)
    source_docs = vectorstore.similarity_search(query_text, k=3)

    # Combine document texts for context
    context_text = "\n\n".join([doc.page_content for doc in source_docs])

    # Fill the prompt
    prompt_input = prompt.format(
        context=context_text,
        question=question,
        code_snippet=code_snippet
    )

    # Generate answer
    response = llm.invoke(prompt_input)

    # Extract sources
    sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]

    return response.content, sources


