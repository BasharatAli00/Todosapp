import os
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

def get_ai_response(user_query: str, todos_from_db: list):
    # 1. Convert database objects into a readable string
    # This acts as our "memory" without needing a vector DB
    todo_context = "\n".join([
        f"- Task: {t.Title}, Description: {t.Description}, Priority: {t.Priority}, Status: {'Done' if t.Complete else 'Pending'}" 
        for t in todos_from_db
    ])

    # 2. Create the prompt with the "stuffed" context
    system_prompt = f"""
    You are an AI Task Assistant. Here are the user's current tasks:
    {todo_context}
    
    Instructions:
    - Answer questions based ONLY on the tasks provided above.
    - If the user asks about a task not listed, politely let them know.
    - Be concise and helpful.
    """

    # 3. Initialize the DeepSeek model
    try:
        model = ChatDeepSeek(
            model="deepseek-chat",
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            temperature=0,
            max_tokens=500,
            timeout=10, # Added timeout for cloud stability
            max_retries=2,
        )
        
        # 4. Invoke the model
        messages = [
            SystemMessage(content=system_prompt), 
            HumanMessage(content=user_query)
        ]
        
        response = model.invoke(messages)
        return response.content # Return just the text content
        
    except Exception as e:
        print(f"AI Service Error: {e}")
        return "I'm sorry, I'm having trouble accessing my AI brain right now."