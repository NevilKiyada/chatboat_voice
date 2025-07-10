"""
Gemini API Client
Handles communication with Google's Gemini AI model
"""

import os
import google.generativeai as genai
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini AI API"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-pro')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Conversation history for context
        self.conversation_history = []
        
        logger.info(f"Gemini client initialized with model: {self.model_name}")
    
    def get_response(self, user_input: str, max_tokens: int = 1000) -> str:
        """
        Get response from Gemini AI
        
        Args:
            user_input: User's message
            max_tokens: Maximum tokens in response
            
        Returns:
            AI response text
        """
        try:
            # Add user input to conversation history
            self.conversation_history.append(f"User: {user_input}")
            
            # Create context from recent conversation
            context = self._build_context()
            
            # Generate response
            response = self.model.generate_content(
                context + f"\nUser: {user_input}\nAssistant:",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )
            
            ai_response = response.text.strip()
            
            # Add AI response to conversation history
            self.conversation_history.append(f"Assistant: {ai_response}")
            
            # Keep only recent conversation (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            logger.info(f"Generated response for user input: {user_input[:50]}...")
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again."
    
    def _build_context(self) -> str:
        """Build conversation context for the AI"""
        context = """You are a helpful voice assistant chatbot. You provide clear, concise, and friendly responses. 
Keep your responses conversational and natural for voice interaction.

Recent conversation:
"""
        
        # Add recent conversation history
        recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
        context += "\n".join(recent_history)
        
        return context
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def set_system_prompt(self, prompt: str):
        """Set a custom system prompt"""
        self.conversation_history.insert(0, f"System: {prompt}")
        logger.info("System prompt updated")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history available."
        
        try:
            history_text = "\n".join(self.conversation_history)
            summary_prompt = f"Please provide a brief summary of this conversation:\n\n{history_text}"
            
            response = self.model.generate_content(summary_prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating conversation summary: {str(e)}")
            return "Unable to generate conversation summary."
