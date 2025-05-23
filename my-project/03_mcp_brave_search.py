import asyncio

from conflux import HandlerChain, Message, handler
from conflux.handlers import McpToolCall, OpenAiLLM
import os

# Get a api key from openai.com
os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"

config = {
    "mcpServers": {
        "fetch": {"url": "http://localhost:9090/brave-search/sse"},
    }
}


@handler
async def fetch_tool_list(msg: Message, chain: HandlerChain) -> str:
    chain.variables["query"] = msg.primary
    return f"User query: {msg.primary}"


@handler
async def answer(msg: Message, chain: HandlerChain) -> str:
    return f"Please answer the following query:\n{chain.variables['query']}\n\nHere is the result from the relevant tool for the query:\n{msg}\n\nProvide a comprehensive answer to the query using the tool result."


def main():
    chain = (
        fetch_tool_list
        >> McpToolCall(config=config, llm=OpenAiLLM)
        >> answer
        >> OpenAiLLM()
    )
    return asyncio.run(
        chain.run(
            "In which year was ISI Hyderabad established? What is the full form of ISI?\n",
        )
    )


if __name__ == "__main__":
    result = main()
    print(result)
