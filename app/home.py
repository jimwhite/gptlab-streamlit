import streamlit as st 
import app_utils as vutil 
import app_component as ac 
import app_user as uv 


st.set_page_config(
    page_title="Fovi",
    page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"#,
    #menu_items={"About": "Fovi is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT-3 language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)


ac.render_cta()

# copies 
home_title = "Fovi"
home_introduction = "Welcome to Fovi, where the power of OpenAI's GPT technology is at your fingertips. Socialize with pre-trained AI Assistants in the Lounge or create your own custom AI companions in the Lab. Whether you need a personal helper, writing partner, or more, Fovi has you covered. Join now and start exploring the endless possibilities!"
home_privacy = "At Fovi, your privacy is our top priority. To protect your personal information, our system only uses the hashed value of your OpenAI API Key, ensuring complete privacy and anonymity. Your API key is only used to access AI functionality during each visit, and is not stored beyond that time. This means you can use Fovi with peace of mind, knowing that your data is always safe and secure."

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.title(home_title)
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)

st.markdown("""\n""")
st.markdown("#### Greetings")
st.write(home_introduction)

#st.markdown("---")
ac.robo_avatar_component()

st.markdown("#### Privacy")
st.write(home_privacy)

st.markdown("""\n""")
st.markdown("""\n""")

st.markdown("#### Get Started")

vu = uv.app_user()
if 'user' not in st.session_state or st.session_state.user['id'] is None:
    vu.view_get_info()
else:
    vu.view_success_confirmation()
    st.write("\n")
    col1, col2 = st.columns(2)
    with col1: 
        if st.button("Hang out with AI Assistants in the Lounge"):
            vutil.switch_page('lounge')
    with col2: 
        if st.button("Create your own AI Assistants in the Lab"):
            vutil.switch_page('lab')

