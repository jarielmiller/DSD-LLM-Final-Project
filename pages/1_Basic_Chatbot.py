import utils
import streamlit as st
from streaming import StreamHandler

from langchain.llms import OpenAI
from langchain.chains import ConversationChain

from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('Basic Chatbot')
st.write('Allows users to interact with the OpenAI LLMs')

if "messages" not in st.session_state:
    st.session_state["messages"] = []

class Basic:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"

    def setup_chain(self):
        # Setup memory for contextual conversation
        llm = OpenAI(model_name=self.openai_model,
                     temperature=0, streaming=True)
        memory = ConversationBufferMemory()
        user = utils.join_messages(st.session_state.messages, 'user')
        assistant = utils.join_messages(st.session_state.messages, 'assistant')
        memory.save_context({"input": user}, {"output":assistant})
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain

    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                try:
                    st_cb = StreamHandler(st.empty())
                    response = chain.run(user_query, callbacks=[st_cb])
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response})
                except Exception as e:
                    print(e)



if __name__ == "__main__":
    obj = Basic()
    obj.main()
