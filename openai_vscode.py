from openai import OpenAI

llm = OpenAI(api_key = "sk-proj-UMyAS2Pr66RML1aalhQtT3BlbkFJ8DiOWalJnyj28C5ZaMOx")
system_prompt = """You are a world class softwar architect"""

user_input = """How to build an API app"""

response = llm.chat.completions.create(
    model = "gpt-3.5-turbo",
    max_tokens = 100,
    temperature = 1,
    messages = [
        {"role": "system", "content":system_prompt},
        {"role": "user", "content":user_input}
    ]
)

print(response.choices[0].message.content)