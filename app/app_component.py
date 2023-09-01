import streamlit as st
import streamlit.components.v1 as c 
import random as r 
import api_bots as ab 
import app_utils as au 

#@st.cache(show_spinner=False, suppress_st_warning=True,ttl=600)
def robo_avatar_component():

    robo_html = "<div style='display: flex; flex-wrap: wrap; justify-content: left;'>"
    robo_avatar_seed = [0, 'aRoN', 'gptLAb', 180, 'nORa', 'dAVe', 'Julia', 'WEldO', 60]

    for i in range(1, 10):
        avatar_url = "https://api.dicebear.com/5.x/bottts-neutral/svg?seed={0}".format(robo_avatar_seed[i-1])#format((i)*r.randint(0,888))
        robo_html += "<img src='{0}' style='width: {1}px; height: {1}px; margin: 10px;'>".format(avatar_url, 50)
    robo_html += "</div>"

    robo_html = """<style>
          @media (max-width: 800px) {
            img {
              max-width: calc((100% - 60px) / 6);
              height: auto;
              margin: 0 10px 10px 0;
            }
          }
        </style>""" + robo_html
    
    c.html(robo_html, height=70)


def st_button(url, label, font_awesome_icon):
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)
    button_code = f'''<a href="{url}" target=_blank><i class="fa {font_awesome_icon}"></i>   {label}</a>'''
    return st.markdown(button_code, unsafe_allow_html=True)


def render_cta():
  with st.sidebar:
      st.write("Let's connect!")
      st_button(url="http://linkedin.com/in/jamespaulwhite/", label="LinkedIn", font_awesome_icon="fa-linkedin")


def view_bot_grid(bot_dict, bots_api=ab.bots_api(), button_disabled=False, show_bot_id=False): 

    col1, col2 = st.columns(2)

    for i in range(0,len(bot_dict)):
        avatar_url = "https://api.dicebear.com/5.x/bottts-neutral/svg?seed={0}".format(bot_dict[i]['name'])
        button_label="Chat with {0}".format(bot_dict[i]['name'])
        button_key="Lounge_bot_{0}".format(bot_dict[i]["id"])
        if i%2 == 0:
            with col1:
                cola, colb = st.columns([1,5])
                cola.image(avatar_url, width=50)
                if show_bot_id == False:
                    colb.markdown(f"{bot_dict[i]['name']} - {bot_dict[i]['tag_line']}")
                else:
                    colb.markdown(f"{bot_dict[i]['name']} - {bot_dict[i]['tag_line']}  \nAssistant ID: {bot_dict[i]['id']}")
            col1.write(bot_dict[i]['description'])
            if 'user'in st.session_state and st.session_state.user['id'] is not None:
                col1.write(f"Session{'s' if bot_dict[i]['sessions_started'] > 1 else ''}: {bot_dict[i]['sessions_started']}")
            if col1.button(button_label, key=button_key, disabled=button_disabled):
                st.session_state.bot_info=bot_dict[i]
                st.session_state.bot_data=bots_api.get_bot(bot_id=bot_dict[i]['id'])
                if st.session_state.bot_info['run_type'] == 'langchain':
                    au.switch_page('langchain')
                else:
                    au.switch_page('assistant')
            col1.write("\n\n")
        else:
            with col2:
                col2a, col2b = st.columns([1,5])
                col2a.image(avatar_url, width=50)
                if show_bot_id == False:
                    col2b.markdown(f"{bot_dict[i]['name']} - {bot_dict[i]['tag_line']}")
                else:
                    col2b.markdown(f"{bot_dict[i]['name']} - {bot_dict[i]['tag_line']}  \nAssistant ID: {bot_dict[i]['id']}")
            col2.write(bot_dict[i]['description'])
            if 'user'in st.session_state and st.session_state.user['id'] is not None:
                col2.write(f"Session{'s' if bot_dict[i]['sessions_started'] > 1 else ''}: {bot_dict[i]['sessions_started']}")
            if col2.button(button_label, key=button_key, disabled=button_disabled):
                st.session_state.bot_info=bot_dict[i]
                st.session_state.bot_data=bots_api.get_bot(bot_id=bot_dict[i]['id'])
                if st.session_state.bot_info['run_type'] == 'langchain':
                    au.switch_page('langchain')
                else:
                    au.switch_page('assistant')
            col2.write("\n\n")
