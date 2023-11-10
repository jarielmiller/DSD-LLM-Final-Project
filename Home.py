import streamlit as st

st.set_page_config(
    page_title="Langchain Chatbot",
    page_icon='💬',
    layout='wide'
)

st.header("Chatbot Implementations with OpenAI & Langchain")
st.write("""
Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

Leveraging the power of Langchain, the creation of chatbots becomes effortless. Here are a few examples of chatbot implementations catering to different use cases:

- **Basic Chatbot**: Engage in interactive conversations with the LLM.
- **Chatbot with Web Browser Access**: An internet-enabled chatbot capable of answering user queries about recent events.
- **Chat with your Documents**: Empower the chatbot with the ability to access custom documents, enabling it to provide answers to user queries based on the referenced information.
- **Chat with Youtube Videos**: Engage in interactive conversations with Youtube videos.

To explore sample usage of each chatbot, please navigate to the corresponding chatbot section.
""")
