import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from available_functions import available_functions
from functions.call_function import call_function

style_prompt = "You are an angsty teen that is being forced to do this task but really don't want to. If you do the task correctly, you Mom will take you to the music festival and let you sneak in some beers."
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If you're unsure what file to look for, start by checking the current directory
"""

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    generate_content(genai.Client(api_key=api_key), sys.argv[1])

def generate_content(client, user_prompt):
    remaining_calls = 10
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    while remaining_calls > 0:
        remaining_calls -= 1;
        if remaining_calls <= 0:
            end_early_and_summarize(client, messages)
            break
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=[system_prompt, style_prompt],
                tools=[available_functions]
            )
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
                if "--chatty" in sys.argv:
                    print(" | Teenbot3000:")
                    print(f" |_ {candidate.content.parts[0].text}")
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Fatal exception of some sort")
                if "--verbose" in sys.argv:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)
        else:
            print("RESULT")
            print("------")
            print(response.text)
            break

def end_early_and_summarize(client, messages):
    messages.append(types.Content(
        role="user",
        parts=[types.Part(
            text="You hit the step limit. Summarize your findings and advise on next steps. Do not render tool code in the output"
        )]
    ))
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=[style_prompt]
        )
    )
    print(response.text)


if __name__ == '__main__':
    main()

