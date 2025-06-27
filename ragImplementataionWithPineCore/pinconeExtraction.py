import os
from dotenv import load_dotenv
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if __name__ == '__main__':

  query = "What is a pineCone?"
  embeddings = PineconeEmbeddings(model="multilingual-e5-large")
  vector_store = PineconeVectorStore(index_name = os.environ['INDEX_NAME'] , embedding= embeddings)
  llm_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=google_api_key,
            temperature=0.1,
        )

  retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
  combine_docs_chain = create_stuff_documents_chain(llm_model,retrival_qa_chat_prompt)
  retival_chain = create_retrieval_chain( retriever= vector_store.as_retriever(),combine_docs_chain=combine_docs_chain)
  result = retival_chain.invoke(input={"input": query})
  print(result)