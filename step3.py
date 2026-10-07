from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


#Python tool
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {path}"


#Gemini tool declaration


TOOL_SCHEMAS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="read_file",
                description="Read a text file and return its contents.",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path of the file to read"
                        }
                    },
                    "required": ["path"]
                }
            )
        ]
    )
]



#Conversation

messages = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text="What is inside notes.txt? Summarize it in one line."
            )
        ]
    )
]



#Agent loop
while True:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=TOOL_SCHEMAS,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )


    #No tool call → final answer
    if not response.function_calls:
        print(response.text)
        break


    #Add Gemini's tool-call message
    message = response.candidates[0].content
    messages.append(message)


  
    #Execute requested tools
    for tool_call in response.function_calls:

        args = tool_call.args

        print(
            f"Model wants to run: "
            f"{tool_call.name}({args})"
        )

        if tool_call.name == "read_file":

            result = read_file(**args)

        else:

            result = f"Unknown tool: {tool_call.name}"


        #Send tool result back to Gemini
        messages.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_function_response(
                        name=tool_call.name,
                        response={
                            "result": result
                        }
                    )
                ]
            )
        )

        print(messages)