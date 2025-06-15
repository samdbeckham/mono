import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_functions import available_functions
from functions.call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=[system_prompt],
            tools=[available_functions]
        )
    )
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Fatal exception of some sort")
            elif "--verbose" in sys.argv:
                print(f"-> {function_call_result.parts[0].function_response.response}")

if __name__ == '__main__':
    main()

