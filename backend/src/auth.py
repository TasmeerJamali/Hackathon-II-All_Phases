"""JWT Authentication Middleware for Better Auth.

Reference: @specs/features/authentication.md
- AC-AUTH-003.1: All API requests require `Authorization: Bearer <token>`
- AC-AUTH-003.2: Invalid token returns 401 Unauthorized
- AC-AUTH-003.3: Expired token returns 401 with "Token expired"
- AC-AUTH-003.4: Backend extracts user_id from token
"""

from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Header, status
from pydantic import BaseModel

from src.config import get_settings


class TokenPayload(BaseModel):
    """JWT token payload from Better Auth."""
    sub: str  # User ID
    email: str | None = None
    name: str | None = None
    exp: int  # Expiration timestamp
    iat: int | None = None  # Issued at


class CurrentUser(BaseModel):
    """Current authenticated user extracted from JWT."""
    id: str
    email: str | None = None
    name: str | None = None


settings = get_settings()


def decode_jwt_token(token: str) -> TokenPayload:
    """
    Decode and verify JWT token issued by Better Auth.
    
    Uses BETTER_AUTH_SECRET shared between frontend and backend.
    """
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None
) -> CurrentUser:
    """
    Extract current user from JWT token in Authorization header.
    
    Per spec AC-AUTH-003.1: All API requests require `Authorization: Bearer <token>`
    
    This is the main dependency for protected routes.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Use: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    payload = decode_jwt_token(token)

    # Check expiration
    if payload.exp < datetime.now(timezone.utc).timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return CurrentUser(
        id=payload.sub,
        email=payload.email,
        name=payload.name,
    )


async def verify_user_access(
    user_id: str,
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """
    Verify the authenticated user matches the requested user_id in URL.
    
    Per spec AC-003.4 and AC-004.3: Cannot access another user's tasks.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access other user's resources",
        )
    return current_user


# Type alias for dependency injection
AuthenticatedUser = Annotated[CurrentUser, Depends(get_current_user)]
