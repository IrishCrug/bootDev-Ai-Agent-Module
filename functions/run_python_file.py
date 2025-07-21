import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
        full_path = os.path.join(working_directory, file_path)
        abso_path = os.path.abspath(full_path)
        working_abs = os.path.abspath(working_directory)


        if not (abso_path == working_abs or abso_path.startswith(working_abs + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(abso_path):
              return f'Error: File "{file_path}" not found.'
        elif not file_path.endswith(".py"):
              return f'Error: "{file_path}" is not a Python file.'
        else:
              try:
                output = subprocess.run(["python", abso_path, *args], capture_output=True, timeout=30, cwd=working_directory)
                if output.returncode != 0:
                    return f"STDOUT: {output.stdout.decode("utf-8")} STDERR: {output.stderr.decode("utf-8")} Process exited with code {output.returncode}"
                elif len(output.stdout.decode("utf-8")) <= 0 and len(output.stderr.decode("utf-8")) <= 0:
                     return "No output produced"
                else:
                     return f"STDOUT: {output.stdout.decode("utf-8")} STDERR: {output.stderr.decode("utf-8")}"
                

              except Exception as e:
                return f"Error: executing Python file: {e}"