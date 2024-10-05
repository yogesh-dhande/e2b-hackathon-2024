from langchain_fireworks import Fireworks
from langchain_core.prompts import ChatPromptTemplate

model = Fireworks(
    model="accounts/fireworks/models/llama-v3p1-405b-instruct", max_tokens=2048
)


def build_simple_agent(system_prompt):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            ("user", "{input}"),
        ]
    )

    chain = prompt | model
    return chain


agent = build_simple_agent("write me a joke about given topic")

def run_agent(prompt):
    return agent.invoke({"input": prompt})
