"""OpenAI Agent for Todo Chatbot.

Reference: @specs/features/chatbot.md
- AC-CHAT-001.1: "Add task to X" → calls add_task tool
- AC-CHAT-001.2: "Show my tasks" → calls list_tasks(status="all")
- AC-CHAT-001.3: "What's pending?" → calls list_tasks(status="pending")
- AC-CHAT-001.4: "Mark task X as done" → calls complete_task
- AC-CHAT-001.5: "Delete task X" → calls delete_task
"""

import json
import os
from typing import Any

from openai import AsyncOpenAI
from sqlmodel.ext.asyncio.session import AsyncSession

from src.mcp_tools import TOOL_DEFINITIONS, MCPToolExecutor

# System prompt for the AI agent
SYSTEM_PROMPT = """You are a helpful Todo assistant. You help users manage their tasks through natural language.

Available commands you can understand:
- "Add a task to buy groceries" → Create a new task
- "Show my tasks" or "List all tasks" → Show all tasks
- "What's pending?" or "Show incomplete tasks" → Show only pending tasks
- "Mark task 3 as done" or "Complete task 3" → Mark a task as complete
- "Delete task 5" or "Remove task 5" → Delete a task
- "Update task 2 to buy milk" → Update a task title

When the user asks "What's pending?" you MUST call list_tasks with status="pending".
When the user says "show my tasks" you MUST call list_tasks with status="all".

Always be friendly and confirm actions with the user.
Format task lists nicely with checkboxes: ✅ for complete, ❌ for pending.
"""


class TodoAgent:
    """OpenAI-powered Todo Agent with function calling.
    
    Uses the tools defined in mcp_tools.py.
    """

    def __init__(self, session: AsyncSession, user_id: str):
        self.session = session
        self.user_id = user_id
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tool_executor = MCPToolExecutor(session, user_id)

    async def chat(
        self,
        user_message: str,
        history: list[dict[str, str]],
    ) -> tuple[str, list[str]]:
        """
        Process a chat message and return response with tool calls.
        
        Per AC-CHAT-002.1: Server holds NO state between requests.
        History is passed in from the database.
        
        Returns: (response_text, list_of_tool_names_called)
        """
        # Build messages array
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        # Call OpenAI with tools
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        choice = response.choices[0]
        tool_calls_made: list[str] = []

        # Process tool calls if any
        if choice.message.tool_calls:
            # Add assistant's message with tool calls
            messages.append(choice.message.model_dump())

            for tool_call in choice.message.tool_calls:
                tool_name = tool_call.function.name
                tool_calls_made.append(tool_name)

                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}

                # Execute the tool
                result = await self.tool_executor.execute_tool(tool_name, arguments)

                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })

            # Get final response after tool execution
            final_response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            response_text = final_response.choices[0].message.content or ""
        else:
            response_text = choice.message.content or ""

        return response_text, tool_calls_made
