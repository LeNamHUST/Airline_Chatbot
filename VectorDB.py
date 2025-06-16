from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

db = Chroma(persist_directory="mydb", embedding_function=OpenAIEmbeddings())