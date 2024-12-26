# serach engine which will provide the answer of your question from wiki , internet , reserch papper 

import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

# Load API Keys
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

# Initialize Tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

search = DuckDuckGoSearchRun(name="search")

# Set Title
st.title("Langchain Search Engine Chatbot")


''' In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.'''

# Session State for Conversation History
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []  # Store entire chat history

# Display Previous Messages
for chat in st.session_state.conversation:
    role = chat["role"]
    question = chat["question"]
    answer = chat["answer"]

    # Display messages based on role
    if role == "user":
        st.chat_message("user").write(question)
    elif role == "assistant":
        st.chat_message("assistant").write(answer)

# User Prompt Input
if Question := st.chat_input(placeholder="Ask me something..."):
    # Append user question
    st.session_state.conversation.append({"role": "user", "question": Question, "answer": ""})
    st.chat_message("user").write(Question)   # user Q is gone then for tht answer it gives 

    # Initialize LLM
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)
    tools = [search, arxiv, wikipedia]

    # Initialize Agent
    search_agent = initialize_agent(
        tools=tools, 
        llm=llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        handle_parsing_errors=True
    )

    # Assistant Response
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(Question, callbacks=[st_cb])

        # Append assistant's response
        st.session_state.conversation.append({"role": "assistant", "question": Question, "answer": response})
        st.write(response)







































# import os 
# import streamlit as st 
# from dotenv import load_dotenv 
# load_dotenv() 

# from langchain_groq import ChatGroq 
# from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper 
# from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun , DuckDuckGoSearchRun 
# from langchain.agents import AgentType , initialize_agent 
# from langchain.callbacks import StreamlitCallbackHandler 

# # we will use our tools 

# arxiv_wrapper =ArxivAPIWrapper(top_k_results=1 , doc_content_chars_max=200) 
# arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper) 

# wikipedia_wraper = WikipediaAPIWrapper(top_k_results=1 , doc_content_chars_max=200) 
# wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_wraper) 

# search = DuckDuckGoSearchRun(name="search") 

# st.title("Langchain search engine Chatbot") 

# ''' In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.'''

# # add your Groq api key 

# st.sidebar.title("Settings") 
# api_key = st.sidebar.text_input("Enter Groq API Key",type="password")


# # now we have to make sure that our  entire conversation should happend along with chat history 
# # we create our session_state 

# if "messages" not in st.session_state :
#     st.session_state["messages"] = [ {"role":"assistant" ,"content":"Hi,iam chatbot who can serach the web. how can i help you ?"} ] # this is the default assistant information  tht we are saving the session_state 
    
# for msg in st.session_state.messages:                                         # then next ,  for every we will go ahed and use it 
#     st.chat_message(msg["role"]).write(msg["content"])                      # wrt every conversation we going to put specific role info inside our session_state as we go ahed 
    

                
# if prompt:= st.chat_input(placeholder="what is genearative ai") :                                        # create prompt by default text msg will be their ,this prompt bydefualt it is having specific placeholder   
#     st.session_state.messages.append({"role":"user" ,"content":prompt})                                    # append the user message to the session_state , so if we ask any query the role will be user& content will be prompt
#     st.chat_message("user").write(prompt)                                                                   # write the user message to the chat  # conclusion : whenever we write any prompt so it will get appended in this particular chat_messages so we can read it 
    
#     llm = ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)                          # inside the prompt we will create our LLm 
#     tools = [search , arxiv , wikipedia]                                                                      # we have our tools
    
#     search_agent = initialize_agent(tools=tools , llm=llm , agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION , handling_parsing_errors=True)    # Now we will convert tools into agent so we able to invoke this 
    
#     with st.chat_message("assistant")  :                                                # whenever assitant is giving me any kind of response then we call streamlitcallbcak handler ,, due tht whever our agent is cummunicate with each other  we able to see that   
#         st_cb = StreamlitCallbackHandler(st.container() ,expand_new_thoughts=False) 
#         response = search_agent.run(st.session_state.messages , callbacks=[st_cb] ) 
#         st.session_state.messages.append({"role":"assistant","content":response})   
#         st.write(response)