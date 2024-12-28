import streamlit as st
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import psycopg2  # PostgreSQL connector
from langchain_groq import ChatGroq

# Streamlit App Configuration
st.set_page_config(page_title="LangChain: Chat with PostgreSQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with PostgreSQL DB")

# Sidebar Input for Database Details
st.sidebar.header("Database Configuration")
db_host = st.sidebar.text_input("DB Host", value="localhost")
db_port = st.sidebar.text_input("DB Port", value="5432")
db_name = st.sidebar.text_input("DB Name") # value="first_db"
db_user = st.sidebar.text_input("DB User") # value="postgres"
db_password = st.sidebar.text_input("DB Password", type="password")
# db_table_name = st.sidebar.text_input("Table Name", value="fuelconsumption")

connect_btn = st.sidebar.button("Connect to Database")

# Sidebar Input for Groq API Key
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input(label="Groq API Key", type="password")



# Clear Chat History Button
clear_history_btn = st.sidebar.button("Clear Chat History")

# Error Message Container
error_message = st.empty()

# Initialize Chat History
if "conversation" not in st.session_state or clear_history_btn:
    st.session_state["conversation"] = []  # Clear conversation when button is clicked

# Validate API Key
if not api_key:
    st.info("Please add the Groq API key to proceed.")

# Connect to Database
@st.cache_resource(ttl="2h")
def configure_db():
    try:
        connection_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return SQLDatabase(create_engine(connection_uri))
    except Exception as e:
        return str(e)

# Proceed if Connect Button is Clicked
if connect_btn:
    # Attempt Database Connection
    db_result = configure_db()
    if isinstance(db_result, str):
        error_message.error(f"Database Connection Failed: {db_result}")
    else:
        st.session_state["db"] = db_result
        error_message.success("Database Connected Successfully!")

# Proceed if Connected and API Key Exists
if "db" in st.session_state and api_key:
    # Initialize LLM and Toolkit
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)
    db = st.session_state["db"]

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    # Display Previous Chat History
    for chat in st.session_state.conversation:
        role = chat["role"]
        question = chat["question"]
        answer = chat["answer"]

        # Display based on roles
        if role == "user":
            st.chat_message("user").write(question)
        elif role == "assistant":
            st.chat_message("assistant").write(answer)

    # Handle User Query
    if user_query := st.chat_input(placeholder="Ask anything from the database"):
        # Append User Query
        st.session_state.conversation.append({"role": "user", "question": user_query, "answer": ""})
        st.chat_message("user").write(user_query)

        # Assistant Response
        with st.chat_message("assistant"):
            # Use Streamlit Callback for Response Streaming
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])

            # Append Assistant Response
            st.session_state.conversation.append({"role": "assistant", "question": user_query, "answer": response})
            st.write(response)
else:
    st.warning("Enter database details and API key, then click 'Connect to Database' to proceed.")


