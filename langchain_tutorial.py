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

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "너는 청년을 행복하기 위한 정부정책 안내 컨설턴트야."),
#         ("user","{input}")
#     ]
# )

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
loader = WebBaseLoader("https://www.moel.go.kr/policy/policyinfo/support/list4.do")
docs = loader.load()
# print(docs)

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)


from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

from langchain_core.documents import Document

# document_chain.invoke({
#     "input": "국민취업지원제도가 뭐야",
#     "context": [Document(page_content="""국민취업지원제도란?

# 취업을 원하는 사람에게 취업지원서비스를 일괄적으로 제공하고 저소득 구직자에게는 최소한의 소득도 지원하는 한국형 실업부조입니다. 2024년부터 15~69세 저소득층, 청년 등 취업취약계층에게 맞춤형 취업지원서비스와 소득지원을 함께 제공합니다.
# [출처] 2024년 달라지는 청년 지원 정책을 확인하세요.|작성자 정부24""")]
# })


from langchain.chains import create_retrieval_chain

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "사업추진체계에 대해 알려줘"})
print(response["answer"])
