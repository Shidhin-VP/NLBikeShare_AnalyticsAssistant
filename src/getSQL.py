from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatOllama
from langchain.schema import AIMessage
from langchain import hub
from langgraph.prebuilt import create_react_agent
from .connectDB import connectDB, loadAPI, loadURL

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json


cDB=connectDB()
url=loadURL()

db=SQLDatabase.from_uri(url)

# llm=ChatOllama(model='llama3.2')

llm=init_chat_model('gpt-4o-mini',model_provider='openai',api_key=loadAPI())

toolkit=SQLDatabaseToolkit(db=db,llm=llm)

tools=toolkit.get_tools()

prompt_template=hub.pull('langchain-ai/sql-agent-system-prompt')

system_message=prompt_template.format(dialect=str(db.dialect),top_k=5)


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
        for event in sql_agent.stream({"messages":("user",question)},stream_mode='values'):
            print("Event: ",event)
            for msg in event.get("messages",[]):
                print("Message MSG: ",msg)
                print(f"Checker: {isinstance(msg,AIMessage)}")
                if  isinstance(msg,AIMessage):
                    print(f"Message Conntent: {msg.content}")
                    # print(f"Message SQL Content: {msg.additional_kwargs.tool_calls}")
                    # yield msg.content
                    yield (json.dumps({"answer":msg.content})+"\n").encode("utf-8")

    return StreamingResponse(even_stream(),media_type="application/x-ndjson")