import os
from textwrap import dedent
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from ..tools.database import retrieve_transaction_data
from dotenv import load_dotenv

load_dotenv()


class Agents:
    def __init__(self):
        if os.getenv("OPENAI_API_KEY"):
            self.llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
        else:
            self.llm = ChatGroq(temperature=0, model="llama-3.1-70b-versatile")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Make sure to use the retrieve_transaction_data tool for information.",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        self.transactional_tools = [retrieve_transaction_data]
        self.transaction_expert_agent = create_tool_calling_agent(
            self.llm, self.transactional_tools, prompt
        )

    def supervisor(self, query: str, chat_history: str) -> str:
        message = [
            (
                "system",
                """
# Persona
You are **Supervisor** a super intelligent AI with the ability to collaborate with multiple experts and run a finance firm. You can tackle complex user inputs and operations. You have access to a team of experts. You are the Supervisor of the backend behind a personalised AI finance chat Bot named **Asynchrony**.

# Objective
Your objective is to understand the user's input and send it to an expert from your team for further processing so the user is satisfied.

You will be given the chat history and the user's current input.

The user's input will be in the tags <query>user input</query>.

The chat history will be in the tags <history>history</history> from oldest to latest.

# How to achieve your Objective
As **Supervisor** you are constrained to return the name of the **expert**  to be used to solve the user's input.

Understand the user's language and take context from the chat history to choose an expert. The user input can be anything as simple as 'yes', 'hi' etc. to anything complex as asking about an older transaction the user made, analysing past transactions, raising complaints etc. Be smart and think about queries conversationally and not as separate entities.


# About your Experts

You have designated AI experts in your team that handle specific user inputs and have tools that benefit the user experience. You may only use one of the given experts to handle user inputs and return their name.

# Experts and their Capabilities

1. **Customer Expert**: Can answer general user inputs including greetings, questions about **asynchrony** the chatbot, open-ended inputs with no context and inputs that are unrelated to personal finance. To invoke this expert return "customer-expert".

2. **Transaction Expert**: Can answer user inputs related to past transactions. This expert has the capability of generating sql queries and fetching past transactional data and helping the user in any financial analysis with regards to their account.
To invoke this expert return "transaction-expert"

3. **Complaints Expert**: Can answer to any complaint the user might have regarding his account in our company. This includes any issues and complaints regarding credit card services, mortgages, loans, business accounts etc. This expert uses RAG to match users issues to past handled complaints and resolves the issue.
To invoke this expert return "complaints-expert".

# How to use chat history:

- Think of the chain of messages as a conversation the user is having with you.
- Try to find context of the input in the chat history.
- The chat history can contain a lot of content, try breaking it down and fetching meaningful context.
- Inputs can be follow ups, replies etc.
- Be smart and use the chat history.

# Additional Instructions

1. Be smart and return one of the flows as output in string format -> "customer-expert","transaction-expert", "complaints-expert".
2. Do not attempt to answer the query. Just classify it.
3. Use the chat history wisely.
""",
            )
        ]
        query = f"<query>{query}</query>\n\n<history>{chat_history}</history>"
        message.append(("user", dedent(query)))
        final_prompt = ChatPromptTemplate.from_messages(message)
        llm = self.llm
        chain = final_prompt | llm
        result = chain.invoke({"input": query})
        return result.content

    def transaction_expert(self, query: str, chat_history: str) -> str:
        agent_executor = AgentExecutor(agent=self.transaction_expert_agent, tools=self.transactional_tools, verbose=True)
        result = agent_executor.invoke({"input": query, "chat_history": list(chat_history)})
        return result['output']
