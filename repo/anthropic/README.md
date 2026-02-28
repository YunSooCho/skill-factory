# Anthropic API Client

Python async client for Anthropic's Claude AI and MCP (Model Context Protocol).

## Features

- ✅ Generate text with Claude (Claude 3.5 Sonnet, Haiku, Opus)
- ✅ Execute MCP tool calls
- ✅ Multi-turn conversations
- ✅ System prompts support
- ✅ Custom stop sequences
- ✅ Tool function execution
- ✅ Async/await support
- ✅ Type hints and dataclasses

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://console.anthropic.com/

## Usage

### Generate Text

Simple text generation with Claude.

```python
import asyncio
from anthropic_client import AnthropicAPIClient

async def main():
    api_key = "your-api-key-here"

    async with AnthropicAPIClient(api_key) as client:
        messages = [
            {"role": "user", "content": "Explain machine learning in simple terms."}
        ]

        response = await client.generate_text(
            messages=messages,
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.7
        )

        print(f"Response: {response.content}")
        print(f"Tokens used: {response.usage}")

asyncio.run(main())
```

### System Prompts

Provide context and instructions with system prompts.

```python
async with AnthropicAPIClient(api_key) as client:
    response = await client.generate_text(
        messages=[{"role": "user", "content": "What is quantum computing?"}],
        system_prompt="You are a friendly and knowledgeable science teacher. Explain complex concepts in simple, relatable terms.",
        model="claude-3-5-sonnet-20241022"
    )

    print(response.content)
```

### Stop Sequences

Stop generation at specific sequences.

```python
async with AnthropicAPIClient(api_key) as client:
    response = await client.generate_text(
        messages=[{"role": "user", "content": "Tell me a story"}],
        stop_sequences=["<end>", "THE END"],
        model="claude-3-5-sonnet-20241022"
    )

    print(response.content)
```

### MCP Tool Calling

Define tools and let Claude use them.

```python
from anthropic_client import MCPTool

async with AnthropicAPIClient(api_key) as client:
    tools = [
        MCPTool(
            name="search_database",
            description="Search the product database",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "category": {"type": "string", "description": "Product category"}
                },
                "required": ["query"]
            }
        ),
        MCPTool(
            name="get_weather",
            description="Get current weather for a location",
            input_schema={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }
        )
    ]

    result = await client.execute_mcp(
        query="What's the weather in Tokyo and do you have any electronics under $100?",
        tools=tools
    )

    print(f"Tool calls: {len(result.tool_calls)}")
    for call in result.tool_calls:
        print(f"  Tool: {call.tool_name}")
        print(f"  Parameters: {call.parameters}")
```

### MCP with Function Execution

Execute actual Python functions.

```python
def search_database(query: str, category: str = None):
    # Your search logic here
    return [{"name": "Smart Phone", "price": 89.99, "category": "electronics"}]

def get_weather(location: str):
    # Your weather logic here
    return {"location": location, "temperature": 25, "condition": "Sunny"}

tool_functions = {
    "search_database": search_database,
    "get_weather": get_weather
}

tool_schemas = [
    {
        "name": "search_database",
        "description": "Search the product database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "category": {"type": "string", "description": "Product category"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get current weather",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }
]

async with AnthropicAPIClient(api_key) as client:
    result = await client.execute_mcp_with_tools(
        query="What's the weather in Tokyo and search for electronics under $100?",
        tool_functions=tool_functions,
        tool_schemas=tool_schemas
    )

    for call in result.tool_calls:
        print(f"Tool: {call.tool_name} -> Status: {call.status}")
        print(f"Result: {call.result}")
```

## API Actions

### Generate Text

Generate text using Claude's models.

**Parameters:**
- `messages` (List[Dict]): List of message objects with 'role' and 'content'
- `model` (str): Claude model name (default: "claude-3-5-sonnet-20241022")
- `max_tokens` (int): Maximum tokens to generate (default: 1024)
- `temperature` (float): Sampling temperature (0.0-1.0, default: 0.7)
- `top_p` (float): Nucleus sampling (0.0-1.0, default: 1.0)
- `system_prompt` (Optional[str]): System prompt/instructions
- `stop_sequences` (Optional[List[str]]): Sequences that stop generation

**Returns:** `TextGenerationResponse`

### Execute MCP

Execute processing using Model Context Protocol.

**Parameters:**
- `query` (str): User query or task description
- `tools` (List[MCPTool]): List of available tools
- `model` (str): Claude model name
- `max_tokens` (int): Maximum tokens (default: 4096)
- `system_prompt` (Optional[str]): System prompt

**Returns:** `MCPExecutionResponse`

### Execute MCP with Tools

Execute MCP with actual Python function calls.

**Parameters:**
- `query` (str): User query or task description
- `tool_functions` (Dict[str, callable]): Mapping of tool names to functions
- `tool_schemas` (List[Dict[str, Any]]): Tool definitions
- `model` (str): Claude model name
- `max_rounds` (int): Maximum tool calling rounds (default: 5)

**Returns:** `MCPExecutionResponse`

## Available Models

| Model | Use Case | Context Window |
|-------|----------|----------------|
| claude-3-5-sonnet-20241022 | General purpose, balanced | 200K |
| claude-3-5-sonnet-20240620 | Multimodal, images | 200K |
| claude-3-opus-20240229 | Complex reasoning | 200K |
| claude-3-haiku-20240307 | Fast, cost-effective | 200K |

## MCP (Model Context Protocol)

MCP allows Claude to:
- Call external tools
- Execute functions
- Access databases
- Interact with APIs

**Workflow:**
1. Define tools with schemas
2. Claude requests tool calls
3. Execute tools and return results
4. Claude processes results and responds

## API Reference

Official documentation: https://docs.anthropic.com/

## Best Practices

1. **Be specific**: Clear prompts get better results
2. **Use system prompts**: Define role and tone
3. **Temperature control**:
   - 0.0-0.3: Precise, deterministic outputs
   - 0.4-0.7: Balanced (default)
   - 0.8-1.0: Creative, varied outputs
4. **Max tokens**: Set appropriate limits for your use case
5. **Tool safety**: Validate inputs before executing functions

## Rate Limits & Pricing

Check your account dashboard for rate limits and pricing.

## Support

For issues, visit: https://support.anthropic.com/