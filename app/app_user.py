import traceback
import streamlit as st
import api_users as au
import api_util_general as gu
import api_util_openai as ou
import logging

legal_prompt = "Ready to explore the endless possibilities of AI? Review and agree to our Terms of Use and Privacy Policy, available on our Terms page. By signing in, you confirm that you have read and agreed to our policies. Let's get started today!"
user_email_prompt = "Please enter your email address: "
user_password_prompt = "Password: "
user_email_invalid = "You entered an invalid email address."
user_email_failed = "Sorry, that email address and password don't match our records."
user_signin_success = "Thanks for signing in! Happy chatting!"
user_signup_success = "Thanks for signing up! Welcome to Fovi Lab! Happy chatting!"
email_placeholder = "Please enter your email address here..."
password_placeholder = "Please enter a unique password here..."


class app_user:
    def __init__(self):
        if 'user' not in st.session_state:
            st.session_state.user = {'id':None, 'user_hash': None, 'email':None, 'api_key':None, 'key_supported_models_list':[]}
        self.container = st.container()
        
    def _get_info(self):
        return st.session_state.user 

    def _set_info(self, user_id, user_hash, email, api_key:None, key_supported_models_list:None):
        st.session_state.user = {'id': user_id, 'email': email, 'user_hash' : user_hash, 'api_key':api_key, 'key_supported_models_list': key_supported_models_list}

    def view_get_info(self):
        with self.container:
            try:
                self._signin_form()
            except Exception as e:
                traceback.print_exc()
                st.error("Something went wrong. Please try again.")

    def _signin_form(self):
        with st.form("signin_form"):
            st.markdown(legal_prompt)
            st.markdown("\n")
                # st.info(user_email_prompt)
            st.text_input(user_email_prompt, key="user_email_input", autocomplete="email", placeholder=email_placeholder)
                # st.info(user_password_prompt)
            st.text_input(user_password_prompt, key="user_password_input", type="password", autocomplete="password", placeholder=password_placeholder)
            st.form_submit_button("Sign In/Up", on_click=self._validate_user_info)

    def _validate_user_info(self):
        u = au.users()

        try:
            email=st.session_state.user_email_input.strip()
            if not email:
                with self.container:
                    st.error("User email cannot be empty.")
                raise u.DBError("Email was empty.")
            password = st.session_state.user_password_input.strip()
            if not password:
                with self.container:
                    st.error("User password cannot be empty.")
                raise u.DBError("Password was empty.")
            user = u.get_create_user(email=email, password_hash=gu.hash_user_string(password))           
            self._set_info(user_id=user['id'], user_hash=user['data']['password_hash'], email=user['data']['email'], api_key=ou.get_openai_api_key(), key_supported_models_list=ou.get_model_names())

        except au.users.UserNotFound:
            with self.container:
                st.error(user_email_failed)
        except u.OpenAIError as e: 
            with self.container:
                st.error(f"{str(e)}")
        except u.DBError as e:
            traceback.print_exc()
            with self.container:
                st.warning("Something went wrong. Please try again.")      

    def view_success_confirmation(self):
        st.write(user_signin_success)


if __name__ == '__main__':
    vu = app_user()
    if 'user' not in st.session_state or st.session_state.user['id'] is None:
        vu.view_get_info()
    else:
        vu.view_success_confirmation()