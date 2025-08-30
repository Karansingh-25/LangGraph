import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

config={'configurable':{'thread_id': 'thread-1'}}

# st.session_state -> dict -> does not get empty every time Enter is Pressed
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []



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


    # response=chatbot.invoke({"message":[HumanMessage(content=user_input)]},config=config)
    # ai_message=response['message'][-1].content
    
    
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {'message':[HumanMessage(content=user_input)]},
                config={'configurable':{'thread_id': 'thread-1'}},
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant',
                                 'content':ai_message})

        # st.text(ai_message)