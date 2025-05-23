import asyncio

from conflux import HandlerChain, Message, handler
from conflux.handlers import McpToolCall, OpenAiLLM
import os

# Get a gemini api key from https://aistudio.google.com/app/apikey
os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"

config = {
    "mcpServers": {
        "fetch": {"url": "http://localhost:9090/fetch/sse"},
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
            "Use the following api pattern `https://api.lyrics.ovh/v1/Anne%20Marie/Birthday` to get the lyrics of the popular song 'Tum hi ho' by Arijit Singh",
        )
    )


if __name__ == "__main__":
    result = main()
    print(result)
