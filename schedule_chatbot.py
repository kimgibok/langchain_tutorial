# 버튼 2개
# 일정추가, 일정관리

# 일정추가를 누르면 
# 날짜: 입력받고 일정: 입력받고  -> content.txt.에 저장

# 일정관리를 누르면
# 채팅을 치게 되는데 어느날의 무슨 일정이 있어? 이런식으로 질문을하면
# content.txt에 있는 내용으로 ai가 일정정리해주기

from dotenv import load_dotenv
import os
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 사용하여 API 키를 불러옵니다.
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4-0125-preview"

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container   # st에 container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)
        
want_to = """너는 아래 내용을 기반으로 일정을 관리해주는 챗봇이야.
content
{}
"""
def open_file():
    with open("content.txt",'r') as f:
        content = f.read()
    return content

# 파일에 일정 추가하는 함수
def add_schedule_to_file(date, event):
    with open("content.txt", "a") as file:
        file.write(f"{date}: {event}\n")
        

content = open_file()


st.header("AI 기반 일정 관리 챗봇")

# 일정 추가 입력 폼
with st.form("schedule_form"):
    date = st.text_input("날짜를 입력하세요 (예: 2023-05-01)")
    event = st.text_input("일정 내용을 입력하세요")
    submit_button = st.form_submit_button("일정 추가")
    if submit_button and date and event:
        add_schedule_to_file(date, event)
        st.success(f"일정 '{event}'가 {date}에 추가되었습니다.")

        
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

