import os
from textwrap import dedent

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from ..tools.database import retrieve_transaction_data

load_dotenv()

directory = os.path.dirname(__file__)
with open(os.path.join(directory, "../prompts/SUPERVISOR.md"), "r") as f:
    SUPERVISOR_PROMPT = f.read()

with open(os.path.join(directory, "../prompts/CUSTOMER_EXPERT.md"), "r") as f:
    CUSTOMER_EXPERT_PROMPT = f.read()

with open(os.path.join(directory, "../prompts/TRANSACTION_EXPERT.md"), "r") as f:
    TRANSACTION_EXPERT_PROMPT = f.read()


class Agents:
    def __init__(self):

        if os.getenv("OPENAI_API_KEY") and os.getenv("PREFFERED_API") != "GROQ":
            from langchain_openai import ChatOpenAI

            self.llm = ChatOpenAI(
                temperature=0,
                model="gpt-4o-mini",
                max_tokens=128000,
            )
            print("Using OpenAI API")
        else:
            from langchain_groq import ChatGroq

            self.llm = ChatGroq(
                temperature=0,
                model="llama-3.1-70b-versatile",
                max_tokens=128000,
            )
            print("Using GROQ API")

    def supervisor(self, query: str, chat_history: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SUPERVISOR_PROMPT,
                ),
                (
                    "user",
                    dedent(
                        f"<query>{query}</query>\n\n<history>{chat_history}</history>"
                    ),
                ),
            ]
        )
        chain = prompt | self.llm
        result = chain.invoke({"input": query})
        return result.content

    def transaction_expert(self, query: str, chat_history: str, user_id: str) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    TRANSACTION_EXPERT_PROMPT,
                ),
                ("system", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        tools = [retrieve_transaction_data]
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
        )
        result = agent_executor.invoke(
            {
                "input": f"User ID {user_id}: " + query,
                "chat_history": list(chat_history),
            }
        )
        return result["output"]

    def customer_expert(self, query: str, chat_history: str):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    CUSTOMER_EXPERT_PROMPT,
                ),
                (
                    "user",
                    dedent(
                        f"<query>{query}</query>\n\n<history>{chat_history}</history>"
                    ),
                ),
            ]
        )
        chain = prompt | self.llm
        result = chain.invoke({"input": query})
        return result.content
