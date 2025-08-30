from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI  
import os
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages


load_dotenv()

def create_llm():
    api_key=os.getenv("GOOGLE_API_KEY")

    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                 api_key=api_key)
    
    return model


llm=create_llm()


class ChatBot(TypedDict):

    message:Annotated[list[HumanMessage],add_messages]

def chat_bot(state:ChatBot):

    # message from state
    messages=state["message"]

    # pass to llm
    response=llm.invoke(messages)

    # append to state
    return {"message":[response]}

checkpoint=MemorySaver()

graph=StateGraph(ChatBot)

graph.add_node("Chat_bot",chat_bot)

graph.add_edge(START,"Chat_bot")
graph.add_edge("Chat_bot",END)

chatbot=graph.compile(checkpointer=checkpoint)
