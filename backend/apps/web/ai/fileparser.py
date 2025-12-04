from openai import OpenAI
from apps.web.util.pdfconverter import FileToPDFConverter
from apps.web.util.fileutils import FileUtils
import os

class FileParser:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def parse_file(self, file_path, prompt=None):
        try:
            # Upload file
            conver_path = FileToPDFConverter.convert(file_path)
            with open(conver_path, "rb") as file:
                uploaded_file = self.client.files.create(
                    file=file, purpose="assistants"
                )
            print(f"===File uploaded successfully, ID===: {uploaded_file.id}")

            # Using the Responses API for analysis
            response = self.client.responses.create(
                model="gpt-4-turbo",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "Extract file content"
                            },
                            {
                                "type": "input_file",
                                "file_id": uploaded_file.id
                            }
                        ]
                    }
                ]
            )
            if file_path != conver_path:
                FileUtils.remove_file(conver_path)
            print("============Responses API============", response.output[0].content[0].text)
            return response.output[0].content[0].text

        except Exception as e:
            return f"错误: {str(e)}"
        
FileParser = FileParser()