import os
import subprocess

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ['python3', full_path],
            timeout=30,
            capture_output=True,
            text=True
        )
        output = [
            f'STDOUT: {result.stdout}',
            f'STDERR: {result.stderr}',
        ]
        if result.returncode != 0:
            output.append(f'Process exited with code: {result.returncode}')
        return '\n'.join(output) if output else "No output produced"
    except Exception as e:
            return f'Error: executing Python file: {e}'

