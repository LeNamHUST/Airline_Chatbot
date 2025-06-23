from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI



def load_vectorstore(path=r"C:\Users\Nam Dao\Desktop\chatbot\data\policy_vectorstore"):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)

def rag(query):
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k":3})
    api_key=''


    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)


    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain({"query":query})

    return result["result"]