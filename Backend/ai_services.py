# ai_service.py
import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser




load_dotenv()

# 1. Initialize Embeddings and Vector Store (Same as before)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="user_todos",
    embedding_function=embeddings,
    persist_directory="./chroma_db" 
)

# 2. Add / Delete Functions (Keep your existing functions here)
def add_todo_to_vector_store(todo_id: int, title: str, description: str, owner_id: int):
    document_text = f"Task Title: {title}\nDescription: {description}"
    metadata = {"todo_id": todo_id, "owner_id": owner_id}
    vector_store.add_texts(texts=[document_text], metadatas=[metadata], ids=[str(todo_id)])
    print(f"Task {todo_id} stored in Vector DB!")

def delete_todo_from_vector_store(todo_id: int):
    try:
        vector_store.delete(ids=[str(todo_id)])
    except Exception as e:
        pass

# 3. NEW: The RAG Chat Function
def ask_ai_about_todos(query: str, owner_id: int) -> str:
    """Retrieves the user's tasks and answers their question."""
    
    # A. Retrieve relevant tasks from the vector database
    # Notice the filter! This ensures User A can't search User B's tasks.
    results = vector_store.similarity_search(
        query=query,
        k=5, # Fetch the top 5 most relevant tasks
        filter={"owner_id": owner_id} 
    )
    
    # B. Format the retrieved tasks into a readable string
    if not results:
        context = "The user currently has no tasks related to this query."
    else:
        context = "\n---\n".join([doc.page_content for doc in results])
        
    # C. Set up the LLM (Requires OPENAI_API_KEY in your environment variables)
    # You can swap this for a local model later if you want!
    model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv('DEEPSEEK_API_KEY'), # Or set DEEPSEEK_API_KEY environment variable
    temperature=0,
    max_tokens=500,
    timeout=None,
    max_retries=2,
)

    
    # D. Create the Prompt Template
    prompt = ChatPromptTemplate.from_template("""
    You are a highly helpful and organized AI task assistant. 
    Use the following retrieved tasks to answer the user's question. 
    If the answer is not in the provided tasks, say "I don't see any tasks matching that description."
    Do not invent tasks that are not in the context.

    User's Tasks (Context):
    {context}

    User's Question:
    {query}
    """)
    
    # E. Create the LangChain Pipeline (Chain) and execute it
    chain = prompt | model | StrOutputParser()
    
    response = chain.invoke({
        "context": context,
        "query": query
    })
    
    return response
# Initialize a lightweight, local embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize ChromaDB - this will create a folder named 'chroma_db' in your backend directory
vector_store = Chroma(
    collection_name="user_todos",
    embedding_function=embeddings,
    persist_directory="./chroma_db" 
)

def add_todo_to_vector_store(todo_id: int, title: str, description: str, owner_id: int):
    """Embeds the task and saves it to ChromaDB with metadata."""
    # Combine title and description to give the AI maximum context
    document_text = f"Task Title: {title}\nDescription: {description}"
    
    # Metadata is CRITICAL so we can filter by owner_id later
    metadata = {
        "todo_id": todo_id,
        "owner_id": owner_id
    }
    
    # We use the string version of the todo_id as the vector ID 
    # so we can easily update or delete it later.
    vector_store.add_texts(
        texts=[document_text], 
        metadatas=[metadata], 
        ids=[str(todo_id)]
    )
    print(f"Task {todo_id} embedded and stored in Vector DB!")

def delete_todo_from_vector_store(todo_id: int):
    """Removes a task from ChromaDB when it's deleted from PostgreSQL."""
    try:
        vector_store.delete(ids=[str(todo_id)])
        print(f"Task {todo_id} removed from Vector DB.")
    except Exception as e:
        print(f"Vector not found or error deleting: {e}")