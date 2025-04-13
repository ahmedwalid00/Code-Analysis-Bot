from src.RagPipeline import final_chain

file_path = "D:\Generative ai\Code Analysis\data"
code_analysis_bot = final_chain(file_path=file_path)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("bye, Have a nice day")
        break
    result = code_analysis_bot.invoke({"question": user_input})

    print(f"\Bot:\n{result['answer']}")
