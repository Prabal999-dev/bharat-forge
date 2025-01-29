import google.generativeai as genai
from flask import jsonify, request
import os
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API key from environment variable

API_KEY = "AIzaSyDDgDljAhNfMavVCX-xD15X2xAQ447YgU8"
if not API_KEY:
    raise ValueError("Missing Google Gemini API key. Set the GOOGLE_API_KEY environment variable.")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Define system prompt for the chatbot
SYSTEM_PROMPT = """You are a knowledgeable business growth assistant for suppliers. 
Your expertise includes:
- Supply chain optimization
- Inventory management
- Market trend analysis
- Pricing strategies
- Customer relationship management
- Quality control
- Digital transformation
- Sustainable practices

Provide specific, actionable advice based on industry best practices. Ensure responses are structured in points or table-like format, concise, and within 100 words."""

class SupplierAssistant:
    def __init__(self):
        try:
            self.chat = model.start_chat(history=[])
            self.initialize_context()
        except Exception as e:
            logging.error(f"Error initializing chatbot: {e}")
            raise RuntimeError("Failed to initialize chatbot")

    def initialize_context(self):
        """Send the system prompt to initialize chat context."""
        try:
            self.chat.send_message(SYSTEM_PROMPT)
            logging.info("Chatbot context initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing chat context: {e}")

    async def get_response(self, user_input: str):
        """Fetch an AI-generated response asynchronously."""
        if not user_input.strip():
            return {
                'status': 'error',
                'response': "User input cannot be empty.",
                'type': 'error'
            }
        
        try:
            response = await asyncio.to_thread(self.chat.send_message, user_input)
            return {
                'status': 'success',
                'response': response.text,
                'type': 'text'
            }
        except Exception as e:
            logging.error(f"Chatbot error: {e}")
            return {
                'status': 'error',
                'response': f"Error processing request: {str(e)}",
                'type': 'error'
            }
