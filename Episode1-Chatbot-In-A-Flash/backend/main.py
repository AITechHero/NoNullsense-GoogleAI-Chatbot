from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from vertex import get_response
import os

app = FastAPI()

# CORS middleware
app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files setup
current_dir = os.path.dirname(os.path.abspath(__file__)) # Directory of this script
frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend") # Directory of the frontend
app.mount("/static", StaticFiles(directory=frontend_dir), name="static") # Mount the frontend directory to /static

class Message(BaseModel): # Pydantic model for the message
    content: str

@app.get("/")
async def read_root():
    """
    Endpoint to serve the index.html file.
    """
    return FileResponse(os.path.join(frontend_dir, "index.html")) # Return the index.html file

@app.post("/chat")
async def chat(message: Message):
    """
    Endpoint to handle chat messages.

    This endpoint receives a chat message, processes it to generate a response,
    and returns the response. If an error occurs during processing, an HTTP 500
    error is raised with the error details.

    Args:
        message (Message): The chat message received from the client.

    Returns:
        dict: A dictionary containing the generated response.

    Raises:
        HTTPException: If an error occurs during message processing, an HTTP 500
        error is raised with the error details.
    """
    try:
        response = await get_response(message.content)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))