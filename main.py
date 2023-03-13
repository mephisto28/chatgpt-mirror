# this code is mainly generated by chatgpt

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chat.chat import Chat

# Create a FastAPI instance
app = FastAPI()

# Mount the static directory containing the frontend code
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Allow CORS for all origins, to make it possible to access the API from a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dictionary to store conversation data
conversations = {}

class Message(BaseModel):
    input: str
    
class Response(BaseModel):
    output: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Define a POST endpoint to handle incoming user messages
@app.post("/api/{conversation_id}")
async def get_response(conversation_id: str, message: Message):
    if conversation_id not in conversations:
        conversations[conversation_id] = Chat(chat_id=conversation_id)
    chat = conversations[conversation_id]
    response = chat.say(message.input)

    return {"output": response}


# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)