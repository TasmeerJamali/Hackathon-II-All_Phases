"""Stateless Chat Endpoint.

Reference: @specs/features/chatbot.md
- AC-CHAT-002.1: Server holds NO state between requests
- AC-CHAT-002.2: Conversation history stored in database
- AC-CHAT-002.3: Each request fetches history from DB

Flow per hackathon spec:
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.agent import TodoAgent
from src.auth import CurrentUser, get_current_user, verify_user_access
from src.database import get_session
from src.models import ChatRequest, ChatResponse, Conversation, Message

router = APIRouter(prefix="/api/{user_id}", tags=["Chat"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    session: SessionDep,
    request: ChatRequest,
    current_user: Annotated[CurrentUser, Depends(verify_user_access)],
) -> ChatResponse:
    """
    Send a message to the AI Todo assistant.
    
    THIS IS A STATELESS ENDPOINT per AC-CHAT-002:
    - Server holds NO state between requests
    - Conversation history is fetched from database
    - Messages are persisted to database
    
    Flow:
    1. Receive message → 2. Load History from DB → 3. Run Agent → 
    4. Store Response → 5. Return
    """
    # Step 1: Get or create conversation
    if request.conversation_id:
        result = await session.execute(
            select(Conversation).where(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id,
            )
        )
        conversation = result.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.flush()

    # Step 2: Fetch conversation history from database (STATELESS)
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    )
    history_messages = result.scalars().all()

    # Build history array for AI agent
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in history_messages
    ]

    # Step 3: Store user message in database
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message,
    )
    session.add(user_message)
    await session.flush()

    # Step 4: Run AI agent with MCP tools
    agent = TodoAgent(session, user_id)
    response_text, tool_calls = await agent.chat(request.message, history)

    # Step 5: Store assistant response in database
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=response_text,
    )
    session.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()

    await session.commit()

    # Step 6: Return response - Server holds NO state now
    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        tool_calls=tool_calls,
    )
