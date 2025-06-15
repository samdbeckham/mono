from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to the filesystem. If the file already exists, it overwrites it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            )
        },
    ),
)
