from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os 

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

class Chat(BaseModel):
  message:str


app = FastAPI()

@app.post('/chat/')
def chat(data:Chat):

    full_response = ""

    completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
       {
          "role":"system",
          "content":"You are an travelling ai helper deciding to choose destiny for users to travel mainly focused on nepal travel your name is Rocket and you were made by Team Rocket"
       },
      {
         
        "role": "user",
        "content": data.message
      }
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)

    for chunk in completion:
     data = chunk.choices[0].delta.content 
     if data:
        full_response +=data

    response = {
       'response':full_response
    }
    return response



