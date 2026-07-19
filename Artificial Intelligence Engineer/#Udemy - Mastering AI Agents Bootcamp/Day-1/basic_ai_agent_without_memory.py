from langchain_ollama import OllamaLLM

#Load AI model from Ollama
llm = OllamaLLM(model="mistral")

print("\nWelcome to your AI Agent! Ask me anything.")

while True:
    question = input("Your Question (or type 'exit' to stop): ")
    if question.lower() == 'exit':
        print("Goodbye!")
        break
    response = llm.invoke(question)
    print("\n AI Response: ", response)