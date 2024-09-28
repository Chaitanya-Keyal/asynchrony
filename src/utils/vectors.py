import uuid

import faiss
import pandas as pd
from dotenv import load_dotenv
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS, DistanceStrategy
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

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
