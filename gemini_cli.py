#!/usr/bin/env python3
"""
A simple command-line interface for interacting with Google's Gemini API.
"""

import os
import sys
import argparse
import textwrap
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def setup_api():
    """Set up the Gemini API with the API key from environment variable."""
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("\nTo use this script, you need to set your Google API key:")
        print("  export GEMINI_API_KEY='your-api-key'")
        print("\nYou can get an API key from https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return False

def get_available_models():
    """Get a list of available Gemini models that support content generation."""
    try:
        models = genai.list_models()
        
        # Filter for models that support content generation
        compatible_models = []
        
        for model in models:
            model_name = model.name
            # Skip embedding models and other non-chat models
            if ("gemini" in model_name and 
                not any(excluded in model_name for excluded in [
                    "embedding", 
                    "vision", 
                    "tts",
                    "native-audio",
                    "thinking"
                ])):
                # Focus on core models known to work well
                if any(core_model in model_name for core_model in [
                    "gemini-1.5-pro", 
                    "gemini-1.5-flash",
                    "gemini-1.0-pro"
                ]):
                    compatible_models.append(model_name)
        
        # If no compatible models found, provide a fallback list
        if not compatible_models:
            return [
                "models/gemini-1.5-flash",
                "models/gemini-1.5-pro",
                "models/gemini-1.0-pro"
            ]
            
        return compatible_models
    except Exception as e:
        print(f"Error listing models: {e}")
        # Return a fallback list of reliable models
        return [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "models/gemini-1.0-pro"
        ]

def create_chat(model_name="models/gemini-1.5-flash"):
    """Create a chat session with the specified model."""
    try:
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        chat = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        ).start_chat(history=[])
        
        return chat
    except Exception as e:
        error_str = str(e)
        if "404" in error_str and "not found" in error_str:
            print(f"Error: Model '{model_name}' is not supported for chat/content generation.")
            print("Try using one of these reliable models instead:")
            print("  - models/gemini-1.5-flash (recommended)")
            print("  - models/gemini-1.5-pro")
            print("  - models/gemini-1.0-pro")
        else:
            print(f"Error creating chat session: {e}")
        return None

def wrap_text(text, width=100):
    """Wrap text to specified width for better readability."""
    wrapped_lines = []
    for line in text.split('\n'):
        if line.strip() == '':
            wrapped_lines.append('')
        else:
            wrapped_lines.extend(textwrap.wrap(line, width=width))
    return '\n'.join(wrapped_lines)

def chat_loop(chat, model_name):
    """Run the interactive chat loop."""
    print(f"\n=== Chat with Gemini ({model_name}) ===")
    print("Type 'exit', 'quit', or press Ctrl+C to end the conversation.")
    print("Type 'clear' to start a new conversation.\n")
    
    try:
        while True:
            user_input = input("\033[1;34m> \033[0m").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting chat.")
                break
                
            if user_input.lower() == 'clear':
                chat = create_chat(model_name)
                print("Chat history cleared.")
                continue
                
            if not user_input:
                continue
                
            try:
                response = chat.send_message(user_input)
                print(f"\n\033[1;32mGemini:\033[0m\n{wrap_text(response.text)}\n")
            except Exception as e:
                error_str = str(e)
                if "429" in error_str and "quota" in error_str.lower():
                    print("\n\033[1;31mRate Limit Error:\033[0m You've reached the API rate limits for the free tier.")
                    print("Tips to resolve this issue:")
                    print("  1. Wait a minute before trying again")
                    print("  2. Try using a different model with '--model models/gemini-1.5-flash-8b'")
                    print("  3. Check your quota at https://ai.google.dev/gemini-api/docs/rate-limits\n")
                else:
                    print(f"\n\033[1;31mError: {e}\033[0m\n")
    except KeyboardInterrupt:
        print("\nExiting chat.")

def list_models_command():
    """List available Gemini models."""
    if not setup_api():
        return
    
    models = get_available_models()
    if models:
        print("\nAvailable Gemini models:")
        for model in models:
            print(f"  - {model}")
    else:
        print("No Gemini models found or could not access the API.")

def main():
    """Main function to parse arguments and run the chat."""
    parser = argparse.ArgumentParser(description='Chat with Google Gemini API')
    parser.add_argument('--model', '-m', type=str, default="models/gemini-1.5-flash", 
                        help='Specify the Gemini model to use')
    parser.add_argument('--list-models', '-l', action='store_true',
                        help='List available Gemini models')
    
    args = parser.parse_args()
    
    if args.list_models:
        list_models_command()
        return
    
    if not setup_api():
        return
    
    chat = create_chat(args.model)
    if chat:
        chat_loop(chat, args.model)

if __name__ == "__main__":
    main()

