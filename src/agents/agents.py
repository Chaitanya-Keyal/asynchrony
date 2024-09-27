from datetime import datetime
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
    
with open(os.path.join(directory, "../prompts/SUMMARISE_COMPLAINT.md"), "r") as f:
    SUMMARISE_COMPLAINT_PROMPT = f.read()


class Agents:
    def __init__(self):

        if os.getenv("OPENAI_API_KEY") and os.getenv("PREFFERED_API") != "GROQ":
            from langchain_openai import ChatOpenAI

            self.llm = ChatOpenAI(
                temperature=0,
                model="gpt-4o-mini",
                max_tokens=16000,
            )
            print("Using OpenAI API")
        else:
            from langchain_groq import ChatGroq

            self.llm = ChatGroq(
                temperature=0,
                model="llama-3.1-70b-versatile",
            )
            print("Using GROQ API")

    def get_prompt(self, agent_prompt, query, chat_history, agent_scratchpad=False):
        prompt = [
            (
                "system",
                agent_prompt,
            ),
            (
                "user",
                dedent(f"<query>{query}</query>\n\n<history>{chat_history}</history>"),
            ),
        ]
        if agent_scratchpad:
            prompt.append(("placeholder", "{agent_scratchpad}"))
        return ChatPromptTemplate.from_messages(prompt)

    def supervisor(self, query: str, chat_history: str) -> str:
        prompt = self.get_prompt(SUPERVISOR_PROMPT, query, chat_history)
        chain = prompt | self.llm
        result = chain.invoke(
            {
                "input": query,
                "current_time": datetime.now().isoformat(),
            }
        )
        return result.content

    def transaction_expert(self, query: str, chat_history: str, user_id: str) -> str:
        prompt = self.get_prompt(
            TRANSACTION_EXPERT_PROMPT, query, chat_history, agent_scratchpad=True
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
                "user_id": user_id,
                "input": query,
                "current_time": datetime.now().isoformat(),
            }
        )
        return result["output"]

    def customer_expert(self, query: str, chat_history: str):
        prompt = self.get_prompt(CUSTOMER_EXPERT_PROMPT, query, chat_history)
        chain = prompt | self.llm
        result = chain.invoke(
            {
                "input": query,
                "current_time": datetime.now().isoformat(),
            }
        )
        return result.content

    def complaints_expert(self, query: str):
        return
    
    def summarise_complaint(self, query: str):
        prompt = self.get_prompt(SUMMARISE_COMPLAINT_PROMPT, query, "")
        chain = prompt | self.llm
        result = chain.invoke(
            {
                "input": query,
                "current_time": datetime.now().isoformat(),
            }
        )
        return result.content

    