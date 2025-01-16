# -*- coding: utf-8 -*-
"""FewShotTemplate_250113.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GUFyZo3LJoPFBUoXpbCc0u8dLaWLFZXm
"""

from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


examples = [
    {
        "question": "스티브 잡스와 아인슈타인 중 누가 더 오래 살았나요?",
        "answer": """이 질문에 추가 질문이 필요한가요: 예.
                     추가 질문: 스티브 잡스는 몇 살에 사망했나요?
                     중간 답변: 스티브 잡스는 56세에 사망했습니다.
                     추가 질문: 아인슈타인은 몇 살에 사망했나요?
                     중간 답변: 아인슈타인은 76세에 사망했습니다.
                     최종 답변은: 아인슈타인
                     """,
    },
    {
        "question": "네이버의 창립자는 언제 태어났나요?",
        "answer": """이 질문에 추가 질문이 필요한가요: 예.
                     추가 질문: 네이버의 창립자는 누구인가요?
                     중간 답변: 네이버는 이해진에 의해 창립되었습니다.
                     추가 질문: 이해진은 언제 태어났나요?
                     중간 답변: 이해진은 1967년 6월 22일에 태어났습니다.
                     최종 답변은: 1967년 6월 22일
                     """,
    },
    {
        "question": "율곡 이이의 어머니가 태어난 해의 통치하던 왕은 누구인가요?",
        "answer": """이 질문에 추가 질문이 필요한가요: 예.
                     추가 질문: 율곡 이이의 어머니는 누구인가요?
                     중간 답변: 율곡 이이의 어머니는 신사임당입니다.
                     추가 질문: 신사임당은 언제 태어났나요?
                     중간 답변: 신사임당은 1504년에 태어났습니다.
                     추가 질문: 1504년에 조선을 통치한 왕은 누구인가요?
                     중간 답변: 1504년에 조선을 통치한 왕은 연산군입니다.
                     최종 답변은: 연산군
                     """,
    },
    {
        "question": "올드보이와 기생충의 감독이 같은 나라 출신인가요?",
        "answer": """이 질문에 추가 질문이 필요한가요: 예.
                     추가 질문: 올드보이의 감독은 누구인가요?
                     중간 답변: 올드보이의 감독은 박찬욱입니다.
                     추가 질문: 박찬욱은 어느 나라 출신인가요?
                     중간 답변: 박찬욱은 대한민국 출신입니다.
                     추가 질문: 기생충의 감독은 누구인가요?
                     중간 답변: 기생충의 감독은 봉준호입니다.
                     추가 질문: 봉준호는 어느 나라 출신인가요?
                     중간 답변: 봉준호는 대한민국 출신입니다.
                     최종 답변은: 예
                     """,
    },
]

example_prompt = PromptTemplate.from_template(
    "Question: {question} Answer: {answer}"
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question:\n{question}\nAnswer:",
    input_variables=["question"],
)

!pip install -qU langchain_openai

question = "Google이 창립된 연도에 Bill Gates의 나이는 몇 살인가요?"

final_prompt = prompt.format(question = question)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    temperature = 0,
    model_name = "gpt-4o",
)

response = llm.invoke(final_prompt)

print(response)

chain = prompt | llm

chain_response = chain.invoke(input = {"현재 대한민국 대통령의 운명은?"})

chain_response

"""# 2. Example Selecter"""

!pip install -qU langchain_chroma

from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    Chroma,
    k = 1,
)

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    temperature = 0,
    model_name = "gpt-4o",
)

prompt = FewShotPromptTemplate(
    example_selector = example_selector,
    example_prompt = example_prompt,
    suffix = "Question:\n{question}\nAnswer:",
    input_variables = ["question"],
)

question = "Google이 창립된 연도에 Bill Gates의 나이는 몇 살인가요?"
example_selector_prompt = prompt.format(question = question)
print(example_selector_prompt)

response = chain.invoke(
    {"question": "Google이 창립된 연도에 Bill Gates의 나이는 몇 살인가요?"}
)

print(response.content)