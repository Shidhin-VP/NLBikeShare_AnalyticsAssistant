from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatOllama
from langchain import hub
from langgraph.prebuilt import create_react_agent
from .connectDB import connectDB, loadAPI, loadURL

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
# from typing import Any, List, Optional
import json

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
    def even_stream():
        try:
            for event in sql_agent.stream({"messages":("user",question)},stream_mode='values'):
                # last_msg=event['messages'][-1]
                # yield (json.dumps({"answer":last_msg.content})+"\n").encode('utf-8')
                print("Event: ",event)
                for msg in event.get("messages",[]):
                    print(f"Checker: {msg.response_metadata==None}")
                    if  msg.role=="assistant":
                        yield (json.dumps({"answer":msg.content})+"\n").encode("utf-8")
        except Exception as e:
            yield f"Error: {e}"

    return StreamingResponse(even_stream(),media_type="application/x-ndjson")