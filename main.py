import os, types, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    
    args = sys.argv[1:]

    system_prompt = """
                    You are a helpful AI coding agent.
                    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
                    - List files and directories
                    - Read file contents
                    - Execute Python files with optional arguments
                    - Write or overwrite files
                    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
                    """


    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        for i in range(20):
            response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
            )
            for can in response.candidates:
                messages.append(can.content)
            
            if response.function_calls:
                 
                if type(response.function_calls) == list:
                    for l in response.function_calls:
                        print(f"Calling function: {l.name}")
                        if "--verbose" in args:
                            results = call_function(l, verbose = True)
                            message_to_add = types.Content(
                                role="tool",
                                parts=[
                                    types.Part.from_function_response(name=l.name, response=results.parts[0].function_response.response)
                                ],
                            )
                            messages.append(message_to_add)
                            if results.parts[0].function_response.response:
                                print(f"-> {results.parts[0].function_response.response}")
                            else:
                                raise Exception ("Error, function call did not return results")
                        else:
                            results = call_function(l)
                            message_to_add = types.Content(
                                role="tool",
                                parts=[
                                    types.Part.from_function_response(name=l.name, response=results.parts[0].function_response.response)
                                ],
                            )
                            messages.append(message_to_add)
                            if not results.parts[0].function_response.response:
                                raise Exception("Error, function call did not return results")
            
            elif response.text:
                print("Final response:")
                print(response.text)
                break
            else:
                break
            i += 1
                        
        
                    
    except Exception as e:
        print (f"Error: {str(e)}")
        
    

    if "--verbose" in args:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            

    

if __name__ == "__main__":
    main()
