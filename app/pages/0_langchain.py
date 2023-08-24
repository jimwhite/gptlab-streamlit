import os
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
import api_util_openai as ou
from pathlib import Path

import streamlit as st
import app_user as vuser

PROMPT_TEMPLATE_PATH = (Path(__file__).parent.parent / "prompt_template.txt").absolute()

page_icon = "🥼"  # 🧠 (brain) 🤖 (robot) 🥼 (lab coat) 📖 (open book) ♾️ (infinity)
st.set_page_config(page_title="Ildebot", page_icon=page_icon)
st.title(f"{page_icon} Ildebot")

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

"""
Ildebot is a Proof of Concept for a virtually intelligent chat agent that guides you in applying SaaSGrowers.com's First UX Framework.
View the [blog post about the First UX Framework](https://saasgrowers.com/blog/the-ultimate-user-onboarding-guide-for-b2b-saas-products/).
"""

if 'user' not in st.session_state or st.session_state.user['id'] is None:
    st.markdown("---")
    # ac.robo_avatar_component()
    st.write("\n")
    uu = vuser.app_user()
    uu.view_get_info()
    st.stop()

@st.cache_data
def get_prompt_template():
    print("Fetching prompt template from file")
    return PROMPT_TEMPLATE_PATH.read_text()

# Choose a model
with st.sidebar:
    model_name = st.selectbox("Choose the OpenAI chat model to use", ou.get_model_names())

# Set up memory
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="history", output_key="output"
)
if len(msgs.messages) == 0:
    # msgs.add_ai_message("How can I help you?")
    # st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]
    msgs.add_ai_message("Hello.  Would you like to explore how to apply First UX Platform to your B2B SaaS?")
    st.session_state.steps = {}

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(avatars[msg.type]):
        # Render intermediate steps if any were saved
        for step in st.session_state.steps.get(str(idx), []):
            if step[0].tool == "_Exception":
                continue
            with st.expander(f"✅ **{step[0].tool}**: {step[0].tool_input}"):
                st.write(step[0].log)
                st.write(f"**{step[1]}**")
        st.write(msg.content)

prompt = PromptTemplate(input_variables=["history", "human_input"], template=get_prompt_template())
llm = ChatOpenAI(openai_api_key=ou.get_openai_api_key(), model_name=model_name, streaming=True)
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory, output_key='output')
print(f'llm_chain.input_keys: {llm_chain.input_keys}')

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

if chat_input := st.chat_input():
    # st.session_state.messages.append(ChatMessage(role="user", content=chat_input))
    st.chat_message("user").write(chat_input)
    with st.chat_message("ai"):
        # st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        st_cb = StreamHandler(st.empty())
        print(f'memory: {memory.memory_variables}')
        print(f'llm_chain.output_keys: {llm_chain.output_keys}')
        response = llm_chain.run({'human_input':chat_input}, callbacks=[st_cb])
        # st.write(response)
        # st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]
        # st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))


# class StreamHandler(BaseCallbackHandler):
#     def __init__(self, container, initial_text=""):
#         self.container = container
#         self.text = initial_text

#     def on_llm_new_token(self, token: str, **kwargs) -> None:
#         self.text += token
#         self.container.markdown(self.text)


# # Set up the LLMChain, passing in memory
# prompt = PromptTemplate(input_variables=["history", "human_input"], template=get_prompt_template())
# stream_handler = StreamHandler(st.empty())
# llm = ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name, streaming=True)
# llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# # If user inputs a new prompt, generate and draw a new response
# if prompt := st.chat_input():
#     st.chat_message("human").write(prompt)
#     # Note: new messages are saved to history automatically by Langchain during run
#     response = llm_chain.run(prompt)
#     st.chat_message("ai").write(response)

# if prompt := st.chat_input():
#     st.chat_message("human").write(prompt)

#     with st.chat_message("ai"):
#         stream_handler = StreamHandler(st.empty())
#         llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4", streaming=True, callbacks=[stream_handler])
#         response = llm_chain.run(prompt, callbacks=[stream_handler])
#         st.chat_message("ai").write(response)
#         # st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))

# llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, streaming=True)
# tools = [DuckDuckGoSearchRun(name="Search")]
# chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools)
# executor = AgentExecutor.from_agent_and_tools(
#     agent=chat_agent,
#     tools=tools,
#     memory=memory,
#     return_intermediate_steps=True,
#     handle_parsing_errors=True,
# )
