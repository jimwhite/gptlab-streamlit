import streamlit as st 
import app_user as uv 
import app_utils as au 


st.set_page_config(
    page_title="Fovi",
    page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"#,
    #menu_items={"About": "Fovi is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT-3 language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)

import app_component as ac 
import api_bots as ab 

ac.render_cta()

# copies 
home_title = "Fovi Lab"
home_introduction = "Welcome to Fovi, where the power of OpenAI's GPT technology is at your fingertips. Socialize with pre-trained AI Assistants in the Lounge or create your own custom AI companions in the Lab. Whether you need a personal helper, writing partner, or more, Fovi has you covered. Join now and start exploring the endless possibilities!"
home_privacy = "Fovi Lab is a demo and under development.  Your personal information such as email, password (in hashed form), and chat history are stored on our servers.  Chat messages and related information are processed by OpenAI and other third-party services."

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.title(home_title)
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><br><font size=5>🚧 Under Construction 🚧</font></span>""",unsafe_allow_html=True)

# st.markdown("""\n""")
st.markdown("#### Greetings")
st.write(home_introduction)

#st.markdown("---")
ac.robo_avatar_component()

st.markdown("#### Privacy")
st.write(home_privacy)

st.markdown("""\n""")

st.markdown("#### Get Started")

b = ab.bots_api()
sb = b.get_bots(is_show_cased=True)

vu = uv.app_user()
if 'user' not in st.session_state or st.session_state.user['id'] is None:
    vu.view_get_info()
    st.write("Come chat with our pre-trained AI assistants.")
    ac.view_bot_grid(bot_dict=sb, bots_api=b, button_disabled=True)
else:
    vu.view_success_confirmation()
    st.write("\n")
    # If we switch to another page like this then the home page can't be seen when logged in.
    # au.switch_page('lounge')
    col1, col2 = st.columns(2)
    with col1: 
        if st.button("Hang out with AI Assistants in the Lounge"):
            au.switch_page('lounge')
    with col2: 
        if st.button("Create your own AI Assistants in the Lab"):
            au.switch_page('lab')
    st.write("Come chat with our pre-trained AI assistants.")
    ac.view_bot_grid(bot_dict=sb, bots_api=b, button_disabled=False)
