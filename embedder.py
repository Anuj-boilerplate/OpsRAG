import os
from google import genai
from chunker import ingest, chunk_documents

path="data.txt"

text=ingest(path)
chunks=chunk_documents(text)
embeddings=[]

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

for chunk in chunks:
    response=client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk["text"]
    )

    embeddings.append(
        response.embeddings[0].values
        )

print (embeddings)