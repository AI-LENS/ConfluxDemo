import asyncio
import os
from typing import Literal

from conflux import HandlerChain, Message, handler
from conflux.handlers import McpToolCall, OpenAiLLM
from pydantic import BaseModel

# Get a api key from openai.com
os.environ["OPENAI_API_KEY"] = "YOUR-API-KEY"

config = {
    "mcpServers": {
        "search": {"url": "http://localhost:9090/brave-search/sse"},
        "yahoo-finance": {"url": "http://localhost:9090/yahoo-finance/sse"},
    }
}


@handler
async def search_ticker_symbol(msg: Message, chain: HandlerChain) -> str:
    chain.variables["stock_query"] = msg.primary
    return f"Search for Yahoo Finance ticker symbol for the company mentioned in the following user query: {msg.primary}?"


class TickerSymbol(BaseModel):
    found: Literal["Yes", "No"]
    symbol: str


@handler
async def get_ticker_symbol(msg: Message, chain: HandlerChain) -> str:
    return (
        f"Your task is to find the Yahoo Finance ticker symbol for '{chain.variables['stock_query']}'.\n"
        f"A simple web search for the company returned the following results:\n{msg}\n\n"
        "Please return ONLY a JSON object in the following format (no extra text):\n"
        "{\n"
        "  \"found\": \"Yes\" | \"No\",\n"
        "  \"symbol\": \"<exact_ticker_symbol>\"\n"
        "}\n\n"
        "Example:\n"
        "{\n  \"found\": \"Yes\",\n  \"symbol\": \"AAPL\"\n}"
    )

@handler
async def find_stock_info(msg: Message, chain: HandlerChain) -> str:
    ticker: TickerSymbol = msg.info["structure"]
    if ticker.found == "No":
        return f"Sorry, Ticker symbol for {chain.variables['stock_query']} could not be found in web search."
    return f"User query {chain.variables["stock_query"]}\n\nTodays Date: 2025-05-23.\n\nFind relevant stock information for {ticker.symbol} from yahoo finance.\n\n"

@handler
async def answer_stock_info(msg: Message, chain: HandlerChain) -> str:
    return f"Please answer the following query:\n{chain.variables['stock_query']}\n\nHere is the result from yahoo finance relevant for the query:\n{msg}\n\nProvide a comprehensive answer to the query using the tool result."


chain = (
    search_ticker_symbol
    >> McpToolCall(config=config, llm=OpenAiLLM)
    >> get_ticker_symbol
    >> OpenAiLLM(structure=TickerSymbol)
    >> find_stock_info
    >> McpToolCall(config=config, llm=OpenAiLLM)
    >> answer_stock_info
    >> OpenAiLLM()
)

res = asyncio.run(
    chain.run(
        "What is the stock price of Shakti Pumps today?",
    )
)
print(res)