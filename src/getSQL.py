from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatOllama
from langchain.schema import AIMessage
from langchain import hub
from langgraph.prebuilt import create_react_agent
# from guardrail import guard
from .connectDB import connectDB, loadAPI, loadURL

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
# from typing import Any, List, Optional
import json

# @guard
# def user_question():
#     """
#     Expected user question:
#     - A natural language string
#     - Must NOT contain SQL keywords like DROP, DELETE, INSERT, UPDATE
#     - Max length 200 characters
#     """
#     pass

cDB=connectDB()
url=loadURL()

db=SQLDatabase.from_uri(url)

llm=ChatOllama(model='llama3.2')

toolkit=SQLDatabaseToolkit(db=db,llm=llm)

tools=toolkit.get_tools()

prompt_template=hub.pull('langchain-ai/sql-agent-system-prompt')

system_message=prompt_template.format(dialect=str(db.dialect),top_k=5)

llm=init_chat_model('gpt-4o-mini',model_provider='openai',api_key=loadAPI())

sql_agent=create_react_agent(llm,tools,prompt=system_message)

app=FastAPI()

class QueryInput(BaseModel):
    question:str

@app.get("/")
async def root():
    return{"message":"API is Up and Running"}

@app.post("/query")
async def stream_answer(query_input:QueryInput):
    question=query_input.question
    # try:
    #     validate=user_question.parse(question)
    #     print("Validate: ",validate)
    # except Exception as e: 
    #     yield f"Input Validation failed: {e}"
    def even_stream():
        for event in sql_agent.stream({"messages":("user",question)},stream_mode='values'):
                # last_msg=event['messages'][-1]
                # yield (json.dumps({"answer":last_msg.content})+"\n").encode('utf-8')
            print("Event: ",event)
            # print(f"event get: {event.get("messages",[])}")
            for msg in event.get("messages",[]):
                print(f"Checker: {isinstance(msg,AIMessage)}")
                if  isinstance(msg,AIMessage):
                    print(f"Message Conntent: {msg.content}")
                    last_msg=event['messages'][-1]
                    yield (json.dumps({"answer":last_msg})+"\n").encode("utf-8")
                else:
                    yield "AI Not Answered, please check OpenAI Limit"


    return StreamingResponse(even_stream(),media_type="application/x-ndjson")