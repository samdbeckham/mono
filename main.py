import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    generate_content(genai.Client(api_key=api_key), sys.argv[1])

def generate_content(client, user_prompt):
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    log(response, user_prompt, "--verbose" in sys.argv)

def log(response, user_prompt, verbose):
    print(response.text)
    if (verbose):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == '__main__':
    main()

