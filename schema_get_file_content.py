from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file within the working directory",
parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get the contents of, relative to the working directory.",
            ),
        },
    ),
)
