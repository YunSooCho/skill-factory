"""
Anthropic API - Claude AI Client

Supports:
- Generate Text
- Execute MCP Processing
"""

import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Message:
    """Claude message"""
    role: str  # 'user', 'assistant', 'system'
    content: str


@dataclass
class TextGenerationResponse:
    """Text generation response from Claude"""
    content: str
    model: str
    stop_reason: str
    stop_sequence: Optional[str]
    usage: Dict[str, int]


@dataclass
class MCPTool:
    """MCP (Model Context Protocol) tool"""
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class MCPToolCall:
    """MCP tool call result"""
    tool_name: str
    parameters: Dict[str, Any]
    result: Any
    status: str


@dataclass
class MCPExecutionResponse:
    """MCP execution response"""
    tool_calls: List[MCPToolCall]
    final_response: str


class AnthropicAPIClient:
    """
    Anthropic API client for Claude AI and MCP.

    API Documentation: https://docs.anthropic.com/
    """

    BASE_URL = "https://api.anthropic.com/v1"
    VERSION = "2023-06-01"

    def __init__(self, api_key: str):
        """
        Initialize Anthropic API client.

        Args:
            api_key: Anthropic API key from console.anthropic.com
        """
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": self.VERSION,
                "content-type": "application/json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate_text(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        system_prompt: Optional[str] = None,
        stop_sequences: Optional[List[str]] = None
    ) -> TextGenerationResponse:
        """
        Generate text using Claude.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Claude model name
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter (0.0-1.0)
            system_prompt: System prompt for Claude
            stop_sequences: Sequences that stop generation

        Returns:
            TextGenerationResponse with generated content

        Raises:
            ValueError: If messages is empty
            aiohttp.ClientError: If request fails
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "messages": messages
        }

        if system_prompt:
            payload["system"] = system_prompt
        if stop_sequences:
            payload["stop_sequences"] = stop_sequences

        async with self.session.post(
            f"{self.BASE_URL}/messages",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Anthropic API error: {error_msg}")

            return TextGenerationResponse(
                content=data["content"][0]["text"],
                model=data.get("model", model),
                stop_reason=data.get("stop_reason", ""),
                stop_sequence=data.get("stop_sequence"),
                usage=data.get("usage", {})
            )

    async def execute_mcp(
        self,
        query: str,
        tools: List[MCPTool],
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> MCPExecutionResponse:
        """
        Execute processing using MCP (Model Context Protocol).

        Args:
            query: User query or task description
            tools: List of available MCP tools
            model: Claude model name
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt

        Returns:
            MCPExecutionResponse with tool calls and final response

        Raises:
            ValueError: If query or tools is empty
            aiohttp.ClientError: If request fails
        """
        if not query:
            raise ValueError("Query cannot be empty")
        if not tools:
            raise ValueError("Tools list cannot be empty")

        # Format tools for API
        tools_payload = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in tools
        ]

        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "tools": tools_payload,
            "messages": messages
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with self.session.post(
            f"{self.BASE_URL}/messages",
            json=payload
        ) as response:
            data = await response.json()

            if response.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                raise Exception(f"Anthropic MCP error: {error_msg}")

            # Extract tool calls and results
            content = data.get("content", [])
            tool_calls = []
            final_response = ""

            for block in content:
                if block.get("type") == "tool_use":
                    tool_calls.append(
                        MCPToolCall(
                            tool_name=block.get("name", ""),
                            parameters=block.get("input", {}),
                            result=None,
                            status="pending"
                        )
                    )
                elif block.get("type") == "text":
                    final_response = block.get("text", "")

            return MCPExecutionResponse(
                tool_calls=tool_calls,
                final_response=final_response
            )

    async def execute_mcp_with_tools(
        self,
        query: str,
        tool_functions: Dict[str, callable],
        tool_schemas: List[Dict[str, Any]],
        model: str = "claude-3-5-sonnet-20241022",
        max_rounds: int = 5
    ) -> MCPExecutionResponse:
        """
        Execute MCP with actual tool function execution.

        Args:
            query: User query or task description
            tool_functions: Dict mapping tool names to Python functions
            tool_schemas: List of tool definitions matching tool_functions
            model: Claude model name
            max_rounds: Maximum tool calling rounds

        Returns:
            MCPExecutionResponse with executed tool calls

        Raises:
            ValueError: If parameters are invalid
            aiohttp.ClientError: If request fails
        """
        messages = [{"role": "user", "content": query}]
        all_tool_calls = []

        for round_num in range(max_rounds):
            # Prepare tools for this round
            mcp_tools = [
                MCPTool(
                    name=schema["name"],
                    description=schema.get("description", ""),
                    input_schema=schema.get("input_schema", {})
                )
                for schema in tool_schemas
            ]

            # Get Claude's response
            mcp_result = await self.execute_mcp(
                query=messages[-1]["content"],
                tools=mcp_tools,
                model=model
            )

            # Check for tool calls
            if not mcp_result.tool_calls:
                return MCPExecutionResponse(
                    tool_calls=all_tool_calls,
                    final_response=mcp_result.final_response
                )

            # Execute tools
            for tool_call in mcp_result.tool_calls:
                tool_name = tool_call.tool_name
                parameters = tool_call.parameters

                if tool_name in tool_functions:
                    try:
                        result = tool_functions[tool_name](**parameters)
                        tool_call.result = result
                        tool_call.status = "success"
                    except Exception as e:
                        tool_call.result = str(e)
                        tool_call.status = "error"

                all_tool_calls.append(tool_call)

                # Add tool result to messages
                tool_result_msg = {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": f"tool_{len(all_tool_calls)}",
                            "content": str(tool_call.result)
                        }
                    ]
                }
                messages.append(tool_result_msg)

        return MCPExecutionResponse(
            tool_calls=all_tool_calls,
            final_response="Max rounds reached"
        )


async def main():
    """Example usage"""
    api_key = "your-api-key-here"

    async with AnthropicAPIClient(api_key) as client:
        # Simple text generation
        messages = [
            {"role": "user", "content": "Explain quantum computing in simple terms."}
        ]

        response = await client.generate_text(
            messages=messages,
            model="claude-3-5-sonnet-20241022",
            max_tokens=500
        )

        print(f"Response: {response.content}")
        print(f"Tokens used: {response.usage}")

        # MCP example
        tools = [
            MCPTool(
                name="calculator",
                description="Perform simple mathematical calculations",
                input_schema={
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            )
        ]

        mcp_result = await client.execute_mcp(
            query="What is 25 * 32?",
            tools=tools
        )

        print(f"Tool calls: {len(mcp_result.tool_calls)}")
        for call in mcp_result.tool_calls:
            print(f"  Tool: {call.tool_name}")
            print(f"  Params: {call.parameters}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())