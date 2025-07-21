import os
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