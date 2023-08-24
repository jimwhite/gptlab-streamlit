import traceback
import streamlit as st
import api_users as au
import api_util_general as gu


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
            st.session_state.user = {'id':None, 'user_hash': None, 'key_supported_models_list':[]}
        self.container = st.container()
        
    def _get_info(self):
        return st.session_state.user 

    def _set_info(self, user_id, email, key_supported_models_list):
        st.session_state.user = {'id': user_id, 'email': email, 'user_hash' : user_id, 'key_supported_models_list': key_supported_models_list}

    def view_get_info(self):
        with self.container:
            st.markdown(legal_prompt)
            st.markdown("\n")
            # st.info(user_email_prompt)
            st.text_input(user_email_prompt, key="user_email_input", placeholder=email_placeholder)
            # st.info(user_password_prompt)
            st.text_input(user_password_prompt, key="user_password_input", type="password", placeholder=password_placeholder)
            st.button("Sign In/Up", key="user_signin_button", on_click=self._validate_user_info)

    def _validate_user_info(self):
        u = au.users()

        try:
            email=gu.normalize_email(st.session_state.user_email_input)
            password = st.session_state.user_password_input.strip()
            if password:
                password_hash=gu.hash_user_string(password)
                user = u.get_create_user(email=email, password_hash=password_hash)           
                self._set_info(user_id=user['id'], email=user['data']['email'], key_supported_models_list=user['data']['supported_models_list'])
            else:
                with self.container:
                    st.error("User password cannot be empty.")
                raise u.DBError("Password was empty.")
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