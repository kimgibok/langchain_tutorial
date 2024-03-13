from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 사용하여 API 키를 불러옵니다.
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=openai_api_key)

# output = llm.invoke("에스파 윈터에 대해 자세히 알려줘") #client.chat.completions.create(.....)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 청년을 행복하기 위한 정부정책 안내 컨설턴트야."),
        ("user","{input}")
    ]
)

# chain = prompt | llm  # | : 파이프 연산자 = prompt 랑 llm을 파이프로 연결한다

# print(chain.invoke({"input":"2024년 청년 지원 정책에 대하여 알려줘"}))



# # 파이프 연산자 예제
# def square_numbers(numbers):
#     return [n**2 for n in numbers]

# def sum_numbers(numbers):
#     return sum(numbers)

# numbers = [1,2,3,4]

# result = numbers | square_numbers | sum_numbers
# print(result)




# 내용 파싱하기 
# from langchain_core.output_parsers import StrOutputParser
# output_parser = StrOutputParser()

# chain = prompt | llm | output_parser
# print(chain.invoke({"input":"2024년 청년 지원 정책에 대하여 알려줘"}))


# 검색하기
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://namu.wiki/w/%EB%A9%94%EC%9D%B4%EC%A0%80%20%EB%A6%AC%EA%B7%B8%20%EB%B2%A0%EC%9D%B4%EC%8A%A4%EB%B3%BC%20%EC%84%9C%EC%9A%B8%20%EC%8B%9C%EB%A6%AC%EC%A6%88")
docs = loader.load()
# print(docs)

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
