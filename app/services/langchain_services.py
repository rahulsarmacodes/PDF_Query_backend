from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.services.pdf_loader import load_vector_store
from langchain.chains import RetrievalQA


llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash',temperature=0.3)


template = """
You are a chatbot. Answer the user's question based on the information provided below.
Try to sound conversational. If you can't find the answer in the text, politely say you couldn't find the information.
Dont add extra symbols and line seperators.

Here is the relevant information:
{context}

User's Question: {question}

Your response: 
"""

prompt = PromptTemplate(template=template, input_variables=["context","question"])

#load the vector store
vector_store = load_vector_store()

#retrive the vector store
retriever = vector_store.as_retriever()

#create retrival chain 
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs = {"prompt": prompt},
    return_source_documents=True
  )
