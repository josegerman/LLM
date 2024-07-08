# working code
# this code uses a local deployed using LM Studio

from openai import OpenAI

llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

system_prompt = """You are a world class softwar architect"""
user_input = """How to build an API app"""

response = llm.chat.completions.create(
    model = "",
    max_tokens = 100,
    temperature = 1,
    messages = [
        {"role": "system", "content":system_prompt},
        {"role": "user", "content":user_input}
    ]
)

print(response.choices[0].message.content)