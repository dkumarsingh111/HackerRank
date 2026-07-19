from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

#Load AI model
llm = OllamaLLM(model="mistral")

#Initialize memory 
chat_history = ChatMessageHistory() #Store user-AI conversation history

#Define AI chat prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Previous Conversation: {chat_history}\nUser: {question}\nAI:"
)


#Function to run AI chat with memory
def run_chain(question):
    #Retrieve chat history manually
    chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages])

    #Run the AI response generation
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

    #Store new user input and AI response in Memory
    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)

    return response


#Interactive CLI Chatbot
print("\n AI Chatbot with Memory")
print("Type 'exit' to stop.")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("\nGoodbye!")
        break

    ai_response = run_chain(user_input)
    print(f"\nAI: {ai_response}")