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