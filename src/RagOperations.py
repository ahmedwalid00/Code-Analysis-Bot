from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

import os
from dotenv import load_dotenv

#Setting openai api key to the enviroment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

#Lodaing data
def loadig_data(file_path) :
    loader = GenericLoader.from_filesystem(
        path=file_path,
        glob="**/*",
        suffixes=['.py'],
        parser=LanguageParser(language=Language.PYTHON)
    )
    
    documents = loader.load()
    return documents


#Splitting data into chunks
def splitting_data_to_chunks(docs) :
    splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON,
                                                            chunk_size=100,
                                                            chunk_overlap=30)
    chunks_of_docs = splitter.split_documents(docs)
    return chunks_of_docs


#getting a retriever from chromadb
def get_retriever(chunks):
    embedding_model = OpenAIEmbeddings()
    vector_db = Chroma.from_documents(documents=chunks,
                                      embedding=embedding_model,
                                      persist_directory="./storage")
    retriever = vector_db.as_retriever(search_kwargs={"k": 4})
    return retriever




