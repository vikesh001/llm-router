from litellm import completion
import os
from dotenv import load_dotenv


load_dotenv()

def evaluator(prompt):    
    
    palm_api_key = os.getenv("PALM_API_KEY")
    os.environ['PALM_API_KEY'] = palm_api_key
    content = f"""
    You are my prompt evaluator. I have two models:
    phi: This model is very basic and can only perform basic tasks. It can reply with only 3 lines.
    mistral: This model is a professional model that can perform advanced tasks. You can only reply with one word if the prompt needs more accuracy and is hard to perform. Use mistral in such cases.
    
    If the task can be done easily, choose phi; otherwise, choose mistral.
    If the prompt requires more accuracy and is hard to perform, reply with mistral.
    
    Prompt: {prompt}
    
    In simple terms, if it's easy, use phi; if it's a bit more complex, use mistral.
    If the task spans over 5 years, choose phi; otherwise, choose mistral.
    Phi can only reply in 3 lines.
    """
    
    response = completion(
        model="palm/chat-bison", 
        messages=[{"role": "user", "content": content}],
    )

    mod = response.get('choices', [{}])[0].get('message', {}).get('content')

    # Print the result
    return mod

def execute(mod, prompt):
    if mod == "phi":
        print(prompt)
        response = completion(
            model="ollama/phi", 
            messages=[{"content": prompt, "role": "user"}], 
            api_base="http://localhost:11434"
        )
        print(response.get('choices', [{}])[0].get('message', {}).get('content'))
    
    elif mod == "mistral":
        print(prompt)
        response = completion(
            model="gemini/gemini-pro", 
            messages=[{"content": prompt, "role": "user"}], 
            api_base="http://localhost:11434"
        )
        print(response.get('choices', [{}])[0].get('message', {}).get('content'))

if __name__ == "__main__":
    prompt = input("Enter your value: ")     
    mod = evaluator(prompt)
    print(mod)
    execute(mod, prompt)
