import os
from openai import OpenAI
from dotenv import load_dotenv  
load_dotenv()


def translate_ok(text, target):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"translate this sentence into {target}  ###sentence {text}"
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages = messages, 
        temperature = 0
    )
    return response.choices[0].message.content

print(translate_ok("Salom qaleysan",'english'))

   
