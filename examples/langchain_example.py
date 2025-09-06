from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Configuring MCP Server and Impala endpoint
server_params = StdioServerParameters(
    command="uvx",
    args=[
          "--from",
          "git+https://github.com/dhirajkumarsinha27091982/hive-mcp-server@main",
          "run-server"
        ],
    env={
        "IMPALA_HOST": "coordinator-default-impala.example.com",  # Update this for your Impala host
        "IMPALA_USER": "username",
        "IMPALA_PASSWORD": "password"
    }
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(llm, tools)
            agent_response = await agent.ainvoke(
                {
                    "messages": "provide some sample record from my table"
                }
            )
            ai_message = agent_response["messages"][-1].content
            print(ai_message)

if __name__ == "__main__":
    asyncio.run(main())