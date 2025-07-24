import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abso_path = os.path.abspath(full_path)
        working_abs = os.path.abspath(working_directory)


        if not (abso_path == working_abs or abso_path.startswith(working_abs + os.sep)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        else:
            dir_path = os.path.dirname(abso_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(abso_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                    
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file, if the file dosent exsit it is created instead and then written too, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
