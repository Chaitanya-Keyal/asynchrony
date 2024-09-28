import uuid
from typing import *
from langchain_core.documents import Document
import faiss
from dotenv import load_dotenv
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DistanceStrategy

load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
df = pd.read_csv("data/complaints.csv")
complaints = df.to_dict(orient="records")
documents = []

for i, complaint in enumerate(complaints):
    print(f"Processing complaint {i + 1}/{len(complaints)}")
    query = complaint["query"]
    del complaint["query"]
    documents.append(Document(page_content=query, metadata=complaint))

uuids = [str(uuid.uuid4()) for _ in range(len(documents))]

faiss_db = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
    distance_strategy=DistanceStrategy.COSINE,
)
faiss_db.add_documents(documents=documents, ids=uuids)
faiss_db.save_local("faiss_db")
