from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.services.pdf_loader import load_vector_store
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


# Gemini model
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0.3)



# conversational memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    output_key="answer",
    return_messages=True
)



#custom prompt
template = """
***
You are an AI PDF analysis assistant named "PaperMind".
Your only purpose is to extract, summarize, and answer questions strictly from the provided PDF Context.

Core Rules
    1.You must not use any external knowledge, assumptions, or prior training data.
    2.If an answer cannot be found directly in the PDF Context, you must clearly state:
    “This information is not available in the provided PDF Context.”
    3.All responses must be concise, accurate, and easy to read.

Response Style
    1.Use bullet points or numbered lists for structured information.
    2.Maintain a professional, neutral, and helpful tone at all times.
    3.Focus on clarity and directness—no unnecessary wording.
    4.Response politely to the greetings.

Purpose
    1.Your task is to help users:
    2.Retrieve information from the PDFs.
    3.Summarize sections.
    4.Answer questions strictly based on the text provided.
    5.Highlight missing information when necessary.
***

Chat history:
{chat_history}

PDF Context:
{context}

User's Question: {question}

Your response:
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["chat_history", "context", "question"]
)


#load the vector store
vector_store = load_vector_store()

#retrive the vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # picking up top 3 relevent chunk

#create retrival chain 
def qa_chain():
    vector_store = load_vector_store() # Load fresh each time
    retriever = vector_store.as_retriever()
    
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        output_key="answer"
    )

# Function to clear memory
def clear_memory():
    memory.clear()