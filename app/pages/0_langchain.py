import os
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
import openai
from pathlib import Path
import streamlit as st

PROMPT_TEMPLATE_PATH = (Path(__file__).parent.parent / "prompt_template.txt").absolute()

page_icon = "🥼"  # 🧠 (brain) 🤖 (robot) 🥼 (lab coat) 📖 (open book) ♾️ (infinity)
st.set_page_config(page_title="Ildebot", page_icon=page_icon)
st.title(f"{page_icon} Ildebot")

# st.set_page_config(
#     page_title="Fovi - Assistant",
#     page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"
# )

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

"""
Ildebot is a Proof of Concept for a virtually intelligent chat agent that guides you in applying SaaSGrowers.com's First UX Framework.
View the [blog post about the First UX Framework](https://saasgrowers.com/blog/the-ultimate-user-onboarding-guide-for-b2b-saas-products/).
"""

# app_desc = '''
# Fovi Demo.
# The user must authorize using a Google account to log in into this application.
# '''
# login_info = login(
#     app_name="Fovi",
#     app_desc=app_desc
# )
# if login_info:
#     user_id, user_email = login_info
#     st.write(f"Welcome {user_email}")
# else:
#     st.info("Please log in to continue")
#     st.stop()

# Get an OpenAI API Key before continuing
if "openai_api_key" in st.secrets:
    openai_api_key = st.secrets.openai_api_key
elif os.environ.get("OPENAI_API_KEY"):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
else:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Enter an OpenAI API Key to continue")
    st.stop()

@st.cache_data(ttl=60 * 60 * 6)
def get_model_names(openai_api_key):
    print("Fetching model names from OpenAI API")
    models = openai.Model.list(openai_api_key=openai_api_key)
    print(f"Fetched {len(models)} models from OpenAI API")
    return [model["id"] for model in models["data"] if model["id"].startswith("gpt")]

@st.cache_data
def get_prompt_template():
    print("Fetching prompt template from file")
    return PROMPT_TEMPLATE_PATH.read_text()

# Choose a model
with st.sidebar:
    model_name = st.selectbox("Choose the OpenAI chat model to use", get_model_names(openai_api_key))

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs)
if len(msgs.messages) == 0:
    # msgs.add_ai_message("How can I help you?")
    msgs.add_ai_message("Hello.  Would you like to explore how to apply First UX Platform to your B2B SaaS?")

view_messages = st.expander("View the message contents in session state")

# Set up the LLMChain, passing in memory
prompt = PromptTemplate(input_variables=["history", "human_input"], template=get_prompt_template())
llm_chain = LLMChain(llm=ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name), prompt=prompt, memory=memory)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    response = llm_chain.run(prompt)
    st.chat_message("ai").write(response)

# From intro above 'You can view the contents of Session State in the expander below.'
# # Draw the messages at the end, so newly generated ones show up immediately
# with view_messages:
#     """
#     Memory initialized with:
#     ```python
#     msgs = StreamlitChatMessageHistory(key="langchain_messages")
#     memory = ConversationBufferMemory(chat_memory=msgs)
#     ```

#     Contents of `st.session_state.langchain_messages`:
#     """
#     view_messages.json(st.session_state.langchain_messages)
