# Getting Started with Conflux

Welcome! This guide will help you set up and use Conflux, a tool for building smart Python programs with AI. No advanced Python knowledge is needed—just follow the steps below.

## 1. Install the Tools You Need

First, we need to install **Conflux**. The easiest way is to use a tool called **uv**.

- [Click here to see how to install uv](https://docs.astral.sh/uv/getting-started/installation/)

## 2. Create a New Project

Open your terminal and run:

```bash
uv init my-project -p 3.13
```

This will make a new folder called `my-project` with everything you need. Move into this folder:

```bash
cd my-project
```

## 3. Set Up Python

Inside your project folder, set up a new Python environment:

```bash
uv venv
```

This creates a `.venv` folder to keep your project’s Python separate from other projects.

## 4. Install Conflux

Now, install Conflux in your project:

```bash
uv pip install conflux-ai
```

## 5. Test Your Setup

Let’s check if everything works. Create a new file called `conflux_test.py` and copy this code into it:

```python
import asyncio
import os

from conflux import HandlerChain, Message, handler
from conflux.handlers import OpenAiLLM

# Get a api key from openai.com
os.environ["GOOGLE_API_KEY"] = "YOUR-API-KEY"

@handler
async def company_name_prompt(msg: Message, chain: HandlerChain) -> str:
    chain.variables["product"] = msg.primary
    return (
        f"What would be an appropriate name for a business specializing in {msg.primary}? "
        "Only mention the company name and nothing else."
    )

@handler
async def company_tagline_prompt(msg: Message, chain: HandlerChain) -> str:
    return (
        f"What would be an appropriate tagline for a business specializing in {chain.variables['product']} "
        f"and with company name {msg.primary}?\nFormat your output like this:\n{msg.primary}: <tagline>"
    )

def main():
    name_and_tagline_generator = (
        company_name_prompt >> OpenAiLLM() >> company_tagline_prompt >> OpenAiLLM()
    )
    res = asyncio.run(name_and_tagline_generator("bike"))
    print(res)

if __name__ == "__main__":
    main()
```

**Note:** Replace `YOUR-API-KEY` with your real API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## 6. Run the Example

In your terminal, run:

```bash
uv run conflux_test.py
```

If everything is set up, you’ll see something like:

```
CycleScapes: Explore the landscape, one pedal stroke at a time.
```

---

You’re all set! You can now start building your own AI-powered Python programs with Conflux. If you get stuck, check the [Conflux documentation](https://github.com/conflux-ai/conflux) or ask for help.
