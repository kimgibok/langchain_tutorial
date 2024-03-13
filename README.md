# langchain_tutorial

# 임베딩 보충 설명
- 자연어 처리의 역사?
## 초기
"I love you"
-> 숫자로 바꾸기 -> 벡터로 만들자
I : [1, 0, 0, 0]
love : [0, 1, 0, 0]
you : [0, 0, 1, 0]
me : [0, 0, 0, 1]

I love you -> vector [[1, 0, 0, 0],[0, 1, 0],[0, 0, 1]]
you love me -> vector[[0, 0, 1],[0, 1, 0],] etc...

## 현재 임베딩 구성 원리
-> 숫자로 바꾸기 -> 벡터로 만들자
렌덤으로 숫자 초깃값을 설정
I : [1.3, 0.1, 0.2, 0.7]
love : [0, 1, 0, 0]
you : [0, 0, 1, 0]
me : [0, 0, 0, 1]

다량의 데이터로 학습 -> 숫자들이 의미를 갖게 됨

## langchain 참고 사이트
https://python.langchain.com/docs/expression_language/cookbook/