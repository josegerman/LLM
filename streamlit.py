
import pandas as pd
import openai
import streamlit as stl
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

#Setting up API key and initializing embedding object with the key.
openai.api_key=("")
embedding=OpenAIEmbeddings(api_key="")

#Initializing the file path to create a dataframe object and return the content in csv to it.
def loading_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        stl.error(f"Error in reading the data file: {e}")
        return pd.DataFrame()
    
#Initializing the dataframe object from the csv file for training the RAG pipeline.
df= loading_data(file_path="./ragtrain.csv")
#checking the df
#print(df)

#Document class to hold text data
class Document:
    def __init__(self,page_content,metadata=None):
        self.page_content=page_content
        self.metadata=metadata

#Preprocess text data into Document objects.
documents = [Document(page_content =text) for text in df['content']]
#Define the persist directory
persist_directory= 'persist_chroma'
#Load documents into chroma vector store
vectordb = Chroma.from_documents(documents=documents,embedding=embedding,persist_directory=persist_directory)
#vectordb.add_documents(documents)

#Initializing ChatOpenAI model by declaring the model name and related parameters.
llm_model = 'gpt-3.5-turbo'
llm = ChatOpenAI(model_name=llm_model, temperature=1, api_key=openai.api_key,organization='org-6StJreD2y9tIMlWLP5d0ahkv')

#Initialize the RetrievalQA chain
qa_chain_default =RetrievalQA.from_chain_type(llm,
                                              retriever=vectordb.as_retriever(search_kwargs={"k":3}),
                                              chain_type="stuff",
                                              return_source_documents=True)

#Streamlit app program.
stl.title("*Ask me anything*")
question= stl.chat_input("Say something")
if question:

    result = qa_chain_default({"query":question})
    source_documents = [doc.page_content for doc in result.get('source_documents',[])]

    stl.write("Query:",result['query'])
    stl.write("Result:",result['result'])
else:
    stl.write("Ask something real!")