# EP1: Chatbot In A Flash ⚡

Difficulty: ⭐ Beginner Friendly | ⏱️ Video: 10 mins | 💪 Practice: ~2 hrs

## Quick Start

```bash
# 1. Activate environment from Episode 0
conda activate google-chatbot

# 2. Install episode requirements
pip install -r requirements.txt

# 3. Get Credentials from Google's Cloud Platform including the Model and Region

1. Change `.env.example` to `.env`
2. Change default values to values from your google cloud project
3. Navigate to Vertex AI > Chat and select the model you want to use
4. Update Location with region and model name with model.

# 4. Start the backend
cd backend
uvicorn main:app --reload

# 5. Open browser and navigate to http://127.0.0.1:8000

# 6. Chatbot Ready
```

## What We're Building

- FastAPI backend with VertexAI integration
- Simple chat interface
- Basic error handling
- Working AI chatbot in under 10 minutes

## Prerequisites

- ✅ Completed Episode 0 setup
- ✅ google-chatbot environment activated
- ✅ Google Cloud account with VertexAI API enabled

## Project Structure

```plaintext
ep1/
├── backend/
│   ├── main.py          # FastAPI application
│   └── vertex.py        # VertexAI client
├── frontend/
│   ├── index.html       # Chat interface
│   ├── styles.css       # Basic styling
│   └── script.js        # Chat functionality
├── .env.example         # rename and update contents
├── requirements.txt     # Additional dependencies
└── README.md           # You are here
```

## Requirements

```txt
# requirements.txt
fastapi==0.68.0
uvicorn==0.15.0
google-cloud-aiplatform==1.35.0
python-dotenv==0.19.0
aiofiles==0.8.0
```

## Implementation Steps

### 1. Backend Setup

```python
# backend/main.py
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
```

```python
# backend/vertex.py
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
import dotenv 
import os

# Load environment variables from .env file
dotenv.load_dotenv()

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"), 
    location=os.getenv("VERTEX_AI_LOCATION")
    )

chat_model = ChatModel.from_pretrained(os.getenv("MODEL_NAME"))

PARAMETERS = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}

async def get_response(message: str) -> str:
    """
    Asynchronously gets a response from the chat model.
    Args:
        message (str): The input message to send to the chat model.
    Returns:
        str: The response text from the chat model.
    Raises:
        Exception: If there is an error in getting the response from VertexAI.
    """
    try:
        chat = chat_model.start_chat(
            context="""You are a helpful AI assistant."""  # You can customize this
        )
        response = chat.send_message(message, **PARAMETERS)
        return response.text
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        raise Exception(f"Failed to get response from VertexAI: {str(e)}")
```

### 2. Frontend Setup

```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div id="chat-container">
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="message-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html> 
```
```javascript
// frontend/script.js
const messageInput = document.getElementById('message-input');
const messagesDiv = document.getElementById('messages');
const sendButton = document.querySelector('button');

// Add enter key listener
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Disable input and button while processing
    messageInput.disabled = true;
    sendButton.disabled = true;

    try {
        // Add user message to chat
        addMessage(message, 'user');
        messageInput.value = '';

        // Send to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: message }),
        });

        const data = await response.json();

        if (response.ok) {
            addMessage(data.response, 'bot');
        } else {
            addErrorMessage(data.detail || 'Failed to get response');
        }
    } catch (error) {
        addErrorMessage('Failed to connect to the server. Please try again.');
    } finally {
        // Re-enable input and button
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function addErrorMessage(text) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = text;
    messagesDiv.appendChild(errorDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
```
```css
/* frontend/styles.css */
#chat-container {
    max-width: 600px;
    margin: 20px auto;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    height: 80vh;
    display: flex;
    flex-direction: column;
}

#messages {
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 20px;
    padding: 10px;
}

.message {
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
    max-width: 80%;
}

.user-message {
    background-color: #007bff;
    color: white;
    margin-left: auto;
}

.bot-message {
    background-color: #f1f1f1;
    color: black;
    margin-right: auto;
}

#input-area {
    display: flex;
    gap: 10px;
}

#message-input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 10px;
    border-radius: 4px;
    margin: 10px 0;
}
```

## Common Issues

- **Error:** "Could not automatically determine credentials..."
  **Fix:** Run `gcloud auth application-default login`

- **Error:** "VertexAI API not enabled"
  **Fix:** Enable API in Google Cloud Console

## Testing Your Implementation

1. Send test message: "Hello, who are you?"
2. Check error handling: Try offline mode
3. Verify response formatting

## Next Steps

→ [Episode 2: Deploy & Defend](../ep2-deploy-and-defend)

- Secure deployment
- Authentication
- Rate limiting

## Need Help?

- Check [Common Issues](#common-issues)
- Join our [Discord](https://discord.gg/7tkhqn6b)
- Watch the [Video Tutorial](https://youtube.com/...)
