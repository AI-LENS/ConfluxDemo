import asyncio
import os

from conflux import HandlerChain, Message, handler
from conflux.handlers import GeminiLLM

# Get a gemini api key from https://aistudio.google.com/app/apikey
os.environ["GOOGLE_API_KEY"] = "YOUR-API-KEY"


@handler
async def company_name_prompt(msg: Message, chain: HandlerChain) -> str:
    chain.variables["product"] = msg.primary
    return (
        f"What would be an appropriate name for a business specializing in {msg.primary}?"
        "Only mention the company name and nothing else."
    )


@handler
async def company_tagline_prompt(msg: Message, chain: HandlerChain) -> str:
    return (
        f"What would be an appropriate tagline for a business specializing in {chain.variables['product']}"
        f" and with company name {msg.primary}?\nFormat your output in the following"
        f" format:\n{msg.primary}: <tagline>"
    )


def main():
    name_and_tagline_generator = (
        company_name_prompt >> GeminiLLM() >> company_tagline_prompt >> GeminiLLM()
    )

    res = asyncio.run(name_and_tagline_generator("bike"))
    print(res)


if __name__ == "__main__":
    main()
