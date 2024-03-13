from dotenv import load_dotenv
import os
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 사용하여 API 키를 불러옵니다.
openai_api_key = os.getenv("OPENAI_API_KEY")

# main.py
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4-0125-preview"

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container   # st에 container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)  # 덧붙인 내용을 container에 추가하겠다

want_to = """너는 아래 내용을 기반으로 질의응답을 하는 로봇이야.
content
{}
"""

content=''''''

st.header("백엔드 스쿨/파이썬 2회차(9기)")
st.info("안녕하세요! 일정을 관리해 주는 챗봇입니다.")
st.error("일정을 관리해주게 설정되어있습니다.")

if "messages" not in st.session_state:  # session state는 실행될때만 모두가 재실행되기때문에 저장할 것을 지정해줌
    st.session_state["messages"] = [ChatMessage(role="assistant", content="안녕하세요! 일정을 관리해 주는 챗봇입니다 어떤 걸 도와드릴까요?")]

for msg in st.session_state.messages: # system user etc...
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():  # input에서 바로 prompt로 적용
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=API_KEY, streaming=True, callbacks=[stream_handler], model_name=MODEL)
        response = llm([ ChatMessage(role="system", content=want_to.format(content))]+st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))