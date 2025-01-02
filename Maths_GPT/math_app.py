from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
from langchain_groq import ChatGroq 
from langchain.chains import LLMMathChain ,LLMChain   # for math calculation 

# to intract with agent 
from langchain.prompts import PromptTemplate 
from langchain_community.utilities import WikipediaAPIWrapper 

from langchain.agents.agent_types import AgentType  
from langchain.agents import Tool , initialize_agent 
from langchain.callbacks import StreamlitCallbackHandler  # the intracttion we able to seee how all the conversaton is 


# set page config 

st.set_page_config(page_title="Text to math problem solver & Data Serch assiatant",page_icon="🪮",layout="wide") 
st.title("Text to math problem solver Using Gemma2 ") 

# Input for GROQ API Key
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = None

groq_api_key = st.sidebar.text_input(label="Enter your GROQ API key", type="password")

submit_key = st.sidebar.button("Submit API Key")

if submit_key:
    st.session_state.groq_api_key = groq_api_key  # Store the API key in session state

# Check if the key is set
if not st.session_state.groq_api_key:
    st.info("Please Add your GROQ API Key and Click Submit to Continue")
    st.stop()
    

llm_model = ChatGroq(model="Gemma2-9b-It" , groq_api_key=groq_api_key) 


#Initialize the tools 

wikipedia_wrapper = WikipediaAPIWrapper() 
wikipedia_tool = Tool(
    name="wikipedia" ,
    func=wikipedia_wrapper.run, 
    description="Search for information on Interner to find various information on the topic mentioned" 
    
)
    
# Initialize the math tools 

math_chain = LLMMathChain.from_llm(llm=llm_model) 
calculator = Tool(
    name="calculator" ,
    func=math_chain.run, 
    description="A tools for answer math related questions. only input mathmatical expression need to be provided" 
) 


your_prompt = """you are a agent your task for solving user mathamtical question.
Logically arrive at the solution and provide the deatials explanation and display it point wise 
for the question below .
Question :{question} 
Answer:"""


prompt_template = PromptTemplate(
    input_variables=["question"] ,
    template=your_prompt
)


#Lets crete the chain which will combine all our tools 
chain=LLMChain(llm=llm_model , prompt=prompt_template) 

# we are adding resoning tools 

reasoning_tool = Tool(
    name="reasoning" , 
    func=chain.run , 
    description="A tool for answerig logic based question and providing the detailed explanation"
) 


# initialize the agents 

assistant_agent = initialize_agent( 
            tools=[calculator , wikipedia_tool , reasoning_tool] ,
            llm=llm_model ,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False ,
            handle_parsing_error=True)



# Clear Conversation Button
if st.sidebar.button("Clear Conversation"):
    # Clear the conversation history in session state
    st.session_state["conversation"] = []
    
    st.session_state.clear()  # Clears all session state variables


# Now crete Our sesssion state  

if "conversation" not in st.session_state: 
    st.session_state["conversation"] = [] 
    
for chat in st.session_state.conversation : 
    role = chat["role"]
    question = chat["question"]
    answer = chat["answer"] 
    
    #Display the msg based on role 
    
    if role=="user":
        st.chat_message("user").write(question) 
    
    if role=="assistant":
        st.chat_message("assistant").write(answer)  
        
        
## Lets start the interaction
question=st.text_area("Enter your Math question here :")  

if st.button("Provide Solution") :
    if question : 
        with st.spinner("Generating.....") :
            st.session_state.conversation.append({"role":"user", "question":question , "answer":" "})
            st.chat_message("user").write(question)   # user Q is gone then for tht it gives  ans  
            
        
        with st.chat_message("assistant"): 
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False) 
            response = assistant_agent.run(question , callbacks=[st_cb]) 
            
            # Append assistant's response 
            st.session_state.conversation.append({"role":"assistant" , "question":question , "answer":response})
            st.write(response) 
            
            
    
    else:
        st.warning("Please enter the question")











# no after submiiting groq api key it again telling me 
# Please Add your GROQ API Key and Click Submit to Continue

# something problem is their 









# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st 
# from langchain_groq import ChatGroq 
# from langchain.chains import LLMMathChain ,LLMChain   # for math calculation 

# # to intract with agent 
# from langchain.prompts import PromptTemplate 
# from langchain_community.utilities import WikipediaAPIWrapper 

# from langchain.agents.agent_types import AgentType  
# from langchain.agents import Tool , initialize_agent 
# from langchain.callbacks import StreamlitCallbackHandler  # the intracttion we able to seee how all the conversaton is 


# # set page config 

# st.set_page_config(page_title="Text to math problem solver & Data Serch assiatant",page_icon="🧮",layout="wide") 
# st.title("Text to math problem solver Using Gemma2 ") 

# groq_api_key = st.sidebar.text_input(label="Enter your GROQ API key" ,type="password") 

# if not groq_api_key :
#     st.info("Plz Add your groq API Key to Continue") 
#     st.stop() 
    

# llm_model = ChatGroq(model="Gemma2-9b-It" , groq_api_key=groq_api_key) 


# #Initialize the tools 

# wikipedia_wrapper = WikipediaAPIWrapper() 
# wikipedia_tool = Tool(
#     name="wikipedia" ,
#     func=wikipedia_wrapper.run, 
#     description="Search for information on Interner to find various information on the topic mentioned" 
    
# )
    
# # Initialize the math tools 

# math_chain = LLMMathChain.from_llm(llm=llm_model) 
# calculator = Tool(
#     name="calculator" ,
#     func=math_chain.run, 
#     description="A tools for answer math related questions. only input mathmatical expression need to be provided" 
# ) 


# your_prompt = """you are a agent your task for solving user mathamtical question.
# Logically arrive at the solution and provide the deatials explanation and display it point wise 
# for the question below .
# Question :{question} 
# Answer:"""


# prompt_template = PromptTemplate(
#     input_variables=["question"] ,
#     template=your_prompt
# )


# #Lets crete the chain which will combine all our tools 
# chain=LLMChain(llm=llm_model , prompt=prompt_template) 

# # we are adding resoning tools 

# reasoning_tool = Tool(
#     name="reasoning" , 
#     func=chain.run , 
#     description="A tool for answerig logic based question and providing the detailed explanation"
# ) 


# # initialize the agents 

# assistant_agent = initialize_agent( 
#             tools=[calculator , wikipedia_tool , reasoning_tool] ,
#             llm=llm_model ,
#             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#             verbose=False ,
#             handle_parsing_error=True)



# # Now crete Our sesssion state  

# # if "message" not in st.session_state:
# #     st.session_state["message"]=[{"role":"assistant","content":"Hi iam chatbot how can i help you today for solving math problem"}]
    
# # for msg in st.session_state.message :
# #     st.chat_message(msg["role"]).write(msg["content"])  
    

# # function to generate response : 
# # def generate_response(question:str) :
# #     response = assistant_agent.invoke({"input":question})
# #     return response 


# if "conversation" not in st.session_state: 
#     st.session_state["conversation"] = [] 
    
# for chat in st.session_state.conversation : 
#     role = chat["role"]
#     question = chat["question"]
#     answer = chat["answer"] 
    
#     #Display the msg based on role 
    
#     if role=="user":
#         st.chat_message("user").write(question) 
    
#     if role=="assistant":
#         st.chat_message("assistant").write(answer)  
        
        
# ## Lets start the interaction
# question=st.text_area("Enter your Math question here :")  

# if st.button("provide solution.") :
#     if question : 
#         with st.spinner("Generating.....") :
#             st.session_state.conversation.append({"role":"user", "question":question , "answer":" "})
#             st.chat_message("user").write(question)   # user Q is gone then for tht it gives  ans  
            
        
#         with st.chat_message("assistant"): 
#             st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False) 
#             response = assistant_agent.run(question , callbacks=[st_cb]) 
            
#             # Append assistant's response 
#             st.session_state.conversation.append({"role":"assistant" , "question":question , "answer":response})
#             st.write(response) 
            
            
    
#     else:
#         st.warning("Please enter the question")

            
            
            
        


 
    
    