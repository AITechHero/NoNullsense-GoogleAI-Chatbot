# EP1: Chatbot In A Flash ⚡

Difficulty: ⭐ Beginner Friendly | ⏱️ Video: 10 mins | 💪 Practice: ~2 hrs

## Quick Start

```bash
# 1. Activate environment from Episode 0
conda activate google-chatbot

# 2. Install episode requirements
pip install -r requirements.txt

# 3. Start the backend
cd backend
uvicorn main:app --reload

# 4. Open frontend/index.html in your browser
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
```

## Implementation Steps

### 1. Backend Setup

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vertex import get_response

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

class Message(BaseModel):
    content: str

@app.post("/chat")
async def chat(message: Message):
    try:
        response = await get_response(message.content)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
```

```python
# backend/vertex.py
from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel

async def get_response(message: str) -> str:
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(message, temperature=0.7)
    return response.text
```

### 2. Frontend Setup

```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>AI Chatbot</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="chat-container">
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="message-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>
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
