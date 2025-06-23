from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

import os
print(os.path.exists(r"C:\Users\Nam Dao\Desktop\chatbot\data\policy.txt"))

loader = TextLoader(r"C:\Users\Nam Dao\Desktop\chatbot\data\policy.txt",  encoding="utf-8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_documents(chunks, embedding_model)

save_path = (r"C:\Users\Nam Dao\Desktop\chatbot\data\policy_vectorstore")
vectorstore.save_local(save_path)

