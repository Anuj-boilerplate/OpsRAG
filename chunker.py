from pathlib import Path
import json
import pandas as pd
from pypdf import PdfReader

def ingest(path):
    ext =Path(path).suffix.lower()

    match ext:
        case '.txt':
            with open(path, "r", encoding="utf-8") as f:
                text=f.read()
                return [{"text":text,"source":path}]
        case ".md":
            with open(path, "r", encoding="utf-8") as f:
                text=f.read();
                return [{"text":text,"source":path}]
        case ".json":
            with open(path, "r", encoding="utf-8") as f:
                text= json.load(f)
                return [{"text":text,"source":path}]
        case ".csv":
            text= pd.read_csv(path)
            return [{"text":text,"source":path}]
        case ".pdf":
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            return [{"text":text,"source":path}]
        case _:
            raise ValueError("Unsupported file type")

def chunk_documents(documents, chunk_size=500):
   chunks=[]
   for doc in documents:
    text=doc["text"]
    for i in range(0, len(text), chunk_size):
        chunk=text[i:i + chunk_size]
        chunks.append({
            "text":chunk,
            "source": doc.get("source")
        })
        return chunks