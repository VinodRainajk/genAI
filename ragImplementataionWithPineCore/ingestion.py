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
    print("hello world")
    loder = TextLoader("F:\Learning\Langchain\docs\mediumblog.txt")
    document = loder.load()
    print("Document is loaded")
    text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")
    embeddings = PineconeEmbeddings(model="multilingual-e5-large")
    print("embeddedin intilize")

    PineconeVectorStore.from_documents(texts,embeddings,index_name = os.environ['INDEX_NAME'])
    print("Done")

