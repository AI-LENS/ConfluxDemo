# More MCP Examples with Conflux

This section demonstrates advanced usage of Conflux with MCP servers, building on the basics from previous tutorials. We’ll walk through two example Python scripts: one for simple web search with MCP, and another for a multi-step agent that combines web search and finance data.

---

## Example 1: Using MCP with Brave Search (`03_mcp_brave_search.py`)

This script shows how to use Conflux with an MCP server that wraps Brave Search. The agent takes a user query, fetches results from Brave Search via MCP, and uses an LLM to generate a comprehensive answer.

**Key Points:**
- Sets up the OpenAI API key.
- Configures the MCP server for Brave Search.
- Defines two handlers:
  - `fetch_tool_list`: Stores the user query.
  - `answer`: Prepares a prompt for the LLM using the tool result.
- Chains the handlers with `McpToolCall` and `OpenAiLLM`.

**Sample usage:**
```python
result = main()
print(result)
```

**What it does:**
- Asks: "In which year was ISI Hyderabad established? What is the full form of ISI?"
- Fetches search results from Brave Search via MCP.
- Uses OpenAI LLM to generate a final answer.

---

## Example 2: Advanced Multi-Tool Agent (`04_advanced_example.py`)

This script demonstrates a more complex agent that:
- Searches for a company’s ticker symbol using web search (Brave Search MCP).
- Extracts the ticker symbol from the search results using an LLM.
- Fetches stock information from Yahoo Finance MCP using the ticker symbol.
- Uses an LLM to generate a comprehensive answer for the user’s query.

**Key Points:**
- Uses a Pydantic model (`TickerSymbol`) to structure the LLM’s output for ticker extraction.
- Chains multiple handlers and tool calls:
  1. `search_ticker_symbol`: Prepares a prompt to search for the ticker symbol.
  2. `McpToolCall` (Brave Search): Performs the web search.
  3. `get_ticker_symbol`: Asks the LLM to extract the ticker symbol from search results.
  4. `OpenAiLLM(structure=TickerSymbol)`: Parses the LLM output as a structured object.
  5. `find_stock_info`: Prepares a prompt to fetch stock info from Yahoo Finance MCP.
  6. `McpToolCall` (Yahoo Finance): Fetches stock data.
  7. `answer_stock_info`: Asks the LLM to generate a final answer using the stock data.
  8. `OpenAiLLM()`: Produces the final user-facing answer.

**Sample usage:**
```python
res = asyncio.run(
    chain.run(
        "What are some latest news on Asian Paints?\n"
    )
)
print(res)
```

**What it does:**
- Handles multi-step queries that require both web search and finance data.
- Demonstrates how to use structured outputs and variable passing between handlers.
- Can be adapted for other multi-tool workflows.

---

**Tip:**
- Replace `YOUR-API-KEY` with your actual OpenAI API key in both scripts.
- Make sure your MCP proxy and relevant servers (Brave Search, Yahoo Finance) are running.

For more details, see the code in `my-project/03_mcp_brave_search.py` and `my-project/04_advanced_example.py`.
