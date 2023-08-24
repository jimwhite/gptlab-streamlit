import api_util_firebase as fu 
import api_util_general as gu 
import api_util_openai as ou
import streamlit as st 

class users:

    class UserNotFound(Exception):
        pass

    class UserHashNotFound(Exception):
        pass

    class BadRequest(Exception):
        pass

    class OpenAIError(Exception):
        def __init__(self, message, error_type=None):
            super().__init__(message)
            self.error_type = error_type 

    class DBError(Exception):
        pass

    def __init__(self):
        self.db = fu.firestore_db()

    def find_user(self, email):
        user_id = gu.email_to_user_id(email)
        user = self.db.get_doc(collection_name="users", document_id=user_id)
        if user:     
            print(f"find_user('{email}'): {user}")
            return user
        else:
            raise self.UserNotFound("User not found")

    def get_user(self, user_id):
        user = self.db.get_doc(collection_name="users", document_id=user_id)
        if user:
            return user
        else:
            raise self.UserNotFound("User not found")

    def get_users(self, user_id=None):
        query_filters=[]

        if user_id:
            query_filters = [("user_id","==",user_id)]

        user_docs = self.db.get_docs(collection_name="users", query_filters=query_filters)

        if user_docs == None:
            raise self.DBError("Users collection empty!")

        return user_docs 


    def update_user_stats(self, user_id, metric_value_pairs):
        user = self.get_user(user_id)
        
        if not user:
            raise self.UserNotFound("User not found")

        if metric_value_pairs == None:
            raise self.BadRequest("Bad request: need to supply (metric, value) pairs")

        for metric_value_pair in metric_value_pairs:
            try:
                float(str(metric_value_pair[1]))
            except:
                raise self.BadRequest("Bad request: need numeric values ")

        for metric_value_pair in metric_value_pairs:
            self.db.increment_document_fields(collection_name="users", document_id=user_id, field_name=metric_value_pair[0], increment=metric_value_pair[1])


    def create_user(self, email, password_hash):
        user_id = gu.email_to_user_id(email)
        users = self.get_users(user_id=user_id)

        if len(users) > 0:
            raise self.BadRequest("Bad request: user exists")

        user_dict = {
            'user_hash': user_id,
            'email': email,
            'password_hash': password_hash,
            'created_date': gu.get_current_time(),
            'last_modified_date': gu.get_current_time(),
            'email_validated': False,
        }

        user_id = self.db.create_doc(collection_name="users", id=user_id, data=user_dict)
        return user_id 


    def find_user_hash(self, user_hash):
        user_hash_doc = self.db.get_doc(collection_name="user_hash", document_id=user_hash)
        if user_hash_doc:     
            return user_hash_doc
        else:
            raise self.UserHashNotFound("User Hash not found")


    def create_user_hash(self, user_hash):
        try:
            user = self.find_user_hash(user_hash=user_hash)
            raise self.BadRequest("Bad request: user hash exists")
        except self.UserHashNotFound:
            pass

        user_hash_dict = {
            'user_hash_type': 'email',
            'created_date': gu.get_current_time()
        }

        user_hash_id = self.db.create_doc(collection_name="user_hash", data=user_hash_dict, id=user_hash)
        return user_hash_id 


    def get_create_user(self, email, password_hash):
        user_id = gu.email_to_user_id(email)

        # first try to create a user_hash document using the hashed key 
        try:
            user = self.get_user(user_id=email)
        except self.UserNotFound:
            # create a user with email for user_id 
            user_id = self.create_user(email=email, password_hash=password_hash)
            # get user details 
            user = self.get_user(user_id=user_id) 
        
        if user['data']['password_hash'] != password_hash:
            raise self.UserNotFound("No match for that email and password.")

        # Add the supported models list to the user object
        user['data']['supported_models_list'] = []
        print(user)
        return user
