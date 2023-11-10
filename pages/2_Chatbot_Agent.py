import utils
import streamlit as st
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, Tool
from langchain.callbacks import StreamlitCallbackHandler

from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

from langchain.tools import PythonREPLTool

from langchain.utilities import ArxivAPIWrapper

st.set_page_config(page_title="ChatWeb", page_icon="🌐")
st.header('Chatbot with Web Browser Access')
st.write('Equipped with internet agent, enables users to ask questions about recent events')


class ChatbotTools:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"

    def setup_agent(self):
        # Define tool
        ddg_search = DuckDuckGoSearchRun()
        wiki_agent = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        python_repl = PythonREPLTool()
        arxiv = ArxivAPIWrapper()

        tools = [
            Tool(
                name="DuckDuckGoSearch",
                func=ddg_search.run,
                description="Useful for when you need to answer questions about current events. You should ask targeted questions",
            ),
            Tool(
                name="Wikipedia",
                func=wiki_agent.run,
                description="Useful for when you need to query about a specific topic, person, or event. You should ask targeted questions",
            ),
            Tool(
                name="Python REPL",
                func=python_repl.run,
                description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you expect output it should be printed out.",
            ),
            Tool(
                name="Arxiv",
                func=arxiv.run,
                description="Useful for when you need to answer questions about research papers, scientific articles, and preprints etc",
            ),
        ]

        # Setup LLM and Agent
        llm = ChatOpenAI(model_name=self.openai_model, streaming=True)
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True
        )
        return agent

    @utils.enable_chat_history
    def main(self):
        agent = self.setup_agent()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                try:
                    st_cb = StreamlitCallbackHandler(st.container())
                    response = agent.run(user_query, callbacks=[st_cb])
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response})
                    st.write(response)
                except Exception as e:
                    print(e)



if __name__ == "__main__":
    obj = ChatbotTools()
    obj.main()
