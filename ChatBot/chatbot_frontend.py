import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid
 


# **************************** Utility functions ****************************
def generate_thread_id():
    id=uuid.uuid4()
    return id

def new_chat():
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['thread_history']:
        st.session_state['thread_history'].append(thread_id)

def show_chat(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['message']



# **************************** Session State ****************************
# st.session_state -> dict -> does not get empty every time Enter is Pressed

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'thread_history' not in st.session_state:
    st.session_state['thread_history'] =[]

add_thread(st.session_state['thread_id'])


# **************************** SideBar UI ****************************

st.sidebar.title("ChatBot with Google Gemini-2.5")

if st.sidebar.button("New Chat"):
    new_chat()

st.sidebar.header("Conversation History")

for threads in st.session_state['thread_history']:
    if st.sidebar.button(str(threads)):
        st.session_state['thread_id'] = threads
        message = show_chat(thread_id=threads)

        temp_message=[]

        for msg in message:
            if isinstance(msg,HumanMessage):
                temp_message.append({'role':'user','content':msg.content})
            else:
                temp_message.append({'role':'assistant','content':msg.content})

        st.session_state['message_history'] = temp_message







#loading converation history
for message in  st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


    


user_input=st.chat_input("Interact with the bot here...")

if user_input:

    st.session_state['message_history'].append({'role':'user',
                                 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)  

    config={'configurable':{'thread_id': st.session_state['thread_id']}}
    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'message':[HumanMessage(content=user_input)]},
                config=config,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant',
                                 'content':ai_message})

        