import os

def get_files_info(working_directory, directory=None):
    target_directory = os.path.join(working_directory, directory) if directory is not None else working_directory
    if not os.path.abspath(target_directory).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    files = map(
        lambda f: __get_file_info(os.path.join(target_directory, f)),
        os.listdir(target_directory)
    )
    return str.join('\n', files)

def __get_file_info(file_path):
    file_name = file_path.split("/")[-1]
    file_size = os.path.getsize(file_path)
    is_dir = os.path.isdir(file_path)
    return f'- {file_name}: file_size={file_size}, is_dir={is_dir}'

