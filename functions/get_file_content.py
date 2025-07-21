import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abso_path = os.path.abspath(full_path)
        working_abs = os.path.abspath(working_directory)


        if not (abso_path == working_abs or abso_path.startswith(working_abs + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        else:
            if not os.path.isfile(abso_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'
            else:
                with open(abso_path, "r") as f:
                    file_content_string = f.read()
                    if len(file_content_string) > MAX_CHARS:
                        truncated_content = file_content_string[:MAX_CHARS]
                        return f"{truncated_content}[...File \'{abso_path}' truncated at {MAX_CHARS} characters"
                    else:
                        return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"