from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.docstore.document import Document
from typing import Iterator
import csv

class SafeCSVLoader(CSVLoader):
    def lazy_load(self) -> Iterator[Document]:
        with open(self.file_path, newline="", encoding=self.encoding) as csvfile:
            csv_reader = csv.DictReader(csvfile, **self.csv_args)
            for i, row in enumerate(csv_reader):
                # 将None转换为空字符串
                processed_row = {k: (v if v is not None else "") for k, v in row.items()}
                content = "\n".join(
                    f"{k.strip()}: {str(v).strip()}" 
                    for k, v in processed_row.items()
                )
                metadata = {"source": self.file_path, "row": i}
                yield Document(page_content=content, metadata=metadata)