import streamlit as st 
import app_component as au

st.set_page_config(
    page_title="Fovi Lab - FAQ",
    page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"#,
    #menu_items={"About": "Fovi Lab is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)


st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

au.render_cta()

st.title("FAQ")

#st.markdown("---")
au.robo_avatar_component()

st.markdown("#### General")
with st.expander("What is Fovi?", expanded=False):
    st.markdown("GPT Lab is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT language model. With Fovi, you can interact with pre-built AI Assistants or create your own by specifying a prompt and OpenAI model parameters. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.")


with st.expander("Why use Fovi instead of Chat GPT?"):
    st.markdown("Fovi aims to be the \"GitLab\" for your favorite prompts, allowing you to save and reuse your favorite prompts as AI Assistants. This eliminates the need to retype the same prompt every time you want to use it. Additionally, you can share your AI Assistants with others without revealing your exact prompt. Since you're using your own OpenAI API key, you don't have to worry about Chat GPT being at capacity.")

with st.expander("What is an OpenAI API Key and why do I need one?"):
    st.markdown("An OpenAI API key is a unique credential that allows you to interact with OpeAI's GPT models. It also serves as your identifier in GPT Lab, allowing us to remember the AI Assistants you have created.")

with st.expander("How can I get an OpenAI API Key?"):
    st.markdown("You can obtain an OpenAI API Key by creating one on the OpenAI website: https://platform.openai.com/account/api-keys")

with st.expander("Why do I need to enter my OpenAI API key each time I use the app?"):
    st.markdown("For security reasons, your actual OpenAI Key is not stored on our servers. Our application only uses it during the duration of your sessions to interact with OpenAI. To keep track of your information, we use a secure one-way hashing algorithm to store a hashed version of your OpenAI API Key, which becomes your unique identifier in our backend data store. This helps ensure the confidentiality and security of your information.")

with st.expander("Does Fovi cost money?"):
    st.markdown("Currently, Fovi itself is free to use. However, you will incur costs for interacting with the OpenAI GPT models, as each API call to the model will be charged. The cost per call is relatively low, and under normal usage, the cost should be minimal. You have full control over the usage and cost of the model, as you are using your own API key. You can monitor your usage and costs through the OpenAI dashboard and adjust your usage accordingly to stay within your budget. The backend infrastructure costs are currently covered by us, and any donation through the \"Buy Me a Coffee\" link is greatly appreciated!")

with st.expander("Why am I getting a 'You exceeded your current quota, please check your plan and billing details.' error?"):
    st.markdown("This error typically indicates you have hit your maximum monthly spend (hard limit) for the API. However, you will likely see this error if you have a free trial API key. For optimal chatting experience, we recommend upgrading to a pay-as-you-go API key by entering your billing information [here](https://platform.openai.com/account/billing/overview). You can learn more about OpenAI API rate limits [here](https://platform.openai.com/docs/guides/rate-limits/overview).")

st.markdown("#### AI Assistant Design")

with st.expander("How do I go about creating my own AI Assistant?"):
    st.markdown("You can create your AI Assistant in the Lab.")

with st.expander("What is the initial prompt?"):
    st.markdown("The initial prompt is the most crucial part of the AI Assistant design, as it sets the context for the conversation and guides the AI's responses. It is the hidden set of instructions for the AI. The initial prompt should clearly convey the topic or task that you would like the AI to focus on during the conversation.")

with st.expander("Do you have some recommendations on how to create good prompts?"):
    st.markdown("""
    Yes, here are few tips to creating effective prompts:  \n
    * Familiarize yourself with the best practices for prompt engineering, as outlined in this OpenAI article: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api  \n
    * When creating a prompt for a Fovi AI Assistant, make sure to include instructions for the Assistant to introduce itself to the user first. This helps ensure a smooth and engaging chat session.  
    * Test out your prompt in the Lab to ensure it accurately conveys the desired topic or task.   
    """)

with st.expander("What contributes to an AI Assistant's personality?"):
    st.markdown("""
    An AI Assistant's personality is primarily determined by the OpenAI language model you choose and the maximum response token length you set, which affects the length of the Assistant's response. You can also further customize the AI's personality through four advanced parameters: temperature, frequency penalty, presence penalty, and top p. These parameters influence the AI's response style, such as its level of creativity, humor, or formality.  \n
    To make it easier for you, we've grouped the four advanced parameters into pre-defined personality profiles: coaching, creative, sarcastic, truthful, and witty. These profiles offer a convenient way to give your AI a specific personality, but you also have the flexibility to tune the four advanced parameters as desired.
    """)

with st.expander("What language models do you support?"):
    st.markdown("""
    We currently support the following OpenAI GPT models: gpt-3.5-turbo-16k, gpt-3.5-turbo, text-davinci-003, text-curie-001, text-babbage-001, and text-ada-001. In addition, we also support gpt-4 and gpt-4-32k (if you have access to them). Each model has its own strengths and weaknesses, and the choice of model should be based on your specific use case. You can find detailed information on each model on https://platform.openai.com/docs/models and pricing information can be found on https://openai.com/api/pricing/.  \n
    In general, gpt-3.5-turbo-16k or gpt-3.5-turbo is a good choice for a general-purpose AI Assistant due to its performance, which is comparable to text-davinci-003, and its cost, which is 10x cheaper than text-davinci-003. Gpt-4 and gpt-4-32k are the newest and most advanced text-based models; however, they are the priciest and are currently in a limited beta, accessible only to those who have been granted access. Text-davinci-003 is capable of handling a wide range of tasks, including natural language understanding and generation, question answering, summarization, and translation, making it a good choice if you need a highly capable language processing system and have a larger budget. Text-curie-001 and text-babbage-001 offer a good balance between performance and cost, and are ideal for specific use cases like answering questions or providing coding assistance.
    """)

with st.expander("What are the four advanced parameters that can fine-tune an AI Assistant's personality?"):
    st.markdown("""The four advanced parameters that can be used to fine-tune an Assistant's personality are temperature, frequency penalty, presence penalty, and top p.  \n
**Temperature** controls the randomness of the model's responses, with a higher temperature leading to more diverse but potentially less coherent responses, and a lower temperature leading to more predictable and coherent responses.  \n
**Frequency** penalty influences how much the model considers the frequency of a word or phrase when generating a response, with a higher frequency penalty encouraging more original responses by discouraging the use of frequent words and phrases.  \n
**Presence** penalty controls how much the model considers the presence of a word or phrase when generating a response, with a higher presence penalty discouraging the use of frequently occurring words and phrases to generate more original responses.  \n
**Top p** determines the fraction of the most likely next tokens to consider when generating a response, with a lower value leading to more diverse and unpredictable responses, and a higher value resulting in more predictable responses.
""")

st.markdown("#### Privacy, Platform Guidelines, and Intellectual Property")

with st.expander("Is my information kept confidential on Fovi?"):
    st.markdown("Yes, we take your privacy and confidentiality very seriously. We do not store any personally identifiable information, and instead use a secure hashing algorithm to store a hashed version of your OpenAI API Key. Additionally, session transcripts are encrypted.")

with st.expander("How does Fovi ensure the security of my information?"):
    st.markdown("""We use the SHA-256 PBKDF2 algorithm, a highly secure one-way hashing algorithm, to hash your OpenAI API Key and store it securely. This ensures that your key is protected and cannot be used for any unauthorized purposes. 
    
Additionally, we use a symmetric AES-128 encryption algorithm, with a unique key for each user, to encrypt your chat transcripts with the AI Assistants.""")

with st.expander("Are there any restrictions on the type of AI Assistants that can be created in Fovi?"):
    st.markdown("""
    Our Terms of Use have outlined some common sense restrictions you should follow. Please review our Terms of Use, available on the Terms page, for more information. 
    Additionally, since our AI Assistants use the OpenAI language models, you should also comply with the [OpenAI Usage policies](https://platform.openai.com/docs/usage-policies).  \n
    We recommend avoiding creating AI Assistants for use in heavily regulated fields, as the legal and ethical implications of such applications can be complex and far-reaching.  \n
    Please note that Fovi does not assume any liability for the use of the AI Assistants you create using the platform. It is your responsibility to ensure that your AI Assistant complies with all applicable laws and regulations, and to use the platform at your own risk.
    """)
with st.expander("Who owns the prompts created in Fovi?"):
    st.markdown("You do! The prompts created by the users in Fovi belong to the users themselves. GPT Lab is a platform that enables users to interact with and create their own AI Assistants powered by OpenAI's language models, and the prompts created by the users in the app are the property of the users themselves. GPT Lab does not claim any ownership or rights to the prompts created by the users.")
