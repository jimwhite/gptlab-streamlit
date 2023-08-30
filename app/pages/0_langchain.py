from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate

from pathlib import Path

import streamlit as st

import app_component as ac 
import app_user as vuser
import api_bots as bots
import api_util_openai as ou
import app_utils as au 

import logging

if 'user' not in st.session_state or st.session_state.user['id'] is None:
    st.markdown("---")
    # ac.robo_avatar_component()
    st.write("\n")
    uu = vuser.app_user()
    uu.view_get_info()
    st.stop()

# centralize logic to go back to the lounge 
def handler_back_to_lounge(): 
    if "bot_info" in st.session_state:
        del st.session_state['bot_info']
    if "session_id" in st.session_state:
        del st.session_state['session_id']
    if "session_bot_id" in st.session_state:
        del st.session_state['session_bot_id']
    if "session_ended" in st.session_state:
        del st.session_state['session_ended']
    if "session_msg_list" in st.session_state:
        del st.session_state['session_msg_list']
    au.switch_page('lounge')

def render_bot_search():
    st.title("AI Assistant")
    st.write("Discover other Assistants in the Lounge, or locate a specific Assistant by its personalized code.")
    #st.markdown("---")
    ac.robo_avatar_component()
    st.write("\n")
    # search_container = st.container()
    # with search_container:
    #     st.text_input("Find an AI Assistant by entering its personalized code", key = "bot_search_input", on_change=handler_bot_search, args=(search_container,))
    # st.write("or")
    if st.button("Back to Lounge"):
        handler_back_to_lounge()

if 'bot_info' not in st.session_state: 
    # first check url_params for asssitant_id 
    # url_params = st.experimental_get_query_params()
    # if bool(url_params) == True and 'assistant_id' in url_params:
    #     if url_params['assistant_id'][0] != "":
    #         bot_found = handler_bot_search(user_search_str=url_params['assistant_id'][0])
    #         if bot_found == False:
    #             st.error("Assistant in URL cannot be found")
    #             st.experimental_set_query_params(assistant_id="")
    #             render_bot_search() 
    #         else: 
    #             # bot found. Get UI to re-render 
    #             st.experimental_rerun()
    # else:
    render_bot_search()
    st.stop()

# logging.info(st.session_state.bot_info)
# logging.info(st.session_state.bot_data)

# if "session_id" not in st.session_state:
#     if "initial_prompt_msg" in st.session_state.bot_info:
#         render_bot_details(st.session_state.bot_info)    
#     else:
#         handler_bot_search(user_search_str=st.session_state.bot_info['id'])
#         render_bot_details(st.session_state.bot_info)    
# else:
#     render_chat_session()

# page_icon = "🥼"  # 🧠 (brain) 🤖 (robot) 🥼 (lab coat) 📖 (open book) ♾️ (infinity)
bot_name = st.session_state.bot_info['name']
avatar_url = "https://api.dicebear.com/5.x/bottts-neutral/svg?seed={0}&size=50".format(bot_name)
st.set_page_config(page_title=f"Fovi: {bot_name} - Chat", page_icon=avatar_url)
st.title(f"Chat with {bot_name} &nbsp; ![]({avatar_url})")

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

# Choose a model
with st.sidebar:
    model_name = st.selectbox("Choose the OpenAI chat model to use", ou.get_model_names())

"""
Proof of Concept for Fovi AI chatbots that have a memory of the conversation history and can use that memory to guide the conversation.
"""

st.markdown(st.session_state.bot_info['description'])

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Set up memory
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="history", output_key="output"
)

if len(msgs.messages) == 0:
    # msgs.add_ai_message("How can I help you?")
    # st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]
    # msgs.add_ai_message("Hello.  Would you like to explore how to apply First UX Platform to your B2B SaaS?")
    msgs.add_ai_message("Hello!")
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

prompt = PromptTemplate(input_variables=["history", "human_input"], template=st.session_state.bot_data['initial_prompt_msg'])
llm = ChatOpenAI(openai_api_key=ou.get_openai_api_key(), model_name=model_name, streaming=True)
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory, output_key='output')
print(f'llm_chain.input_keys: {llm_chain.input_keys}')

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
