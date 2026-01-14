import os
from typing import Any, Dict, Set

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.auth.keycloak import decode_token, extract_roles, load_keycloak_settings
from src.db.database import get_db_session


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Dict[str, Any]:
    if os.getenv("AUTH_DISABLED", "false").lower() == "true":
        return {
            "sub": "test-user",
            "username": "test-user",
            "email": "test@example.com",
            "roles": {"tester"},
            "claims": {},
        }
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    try:
        claims = await decode_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    settings = load_keycloak_settings()
    roles = extract_roles(claims, settings.client_id)
    return {
        "sub": claims.get("sub"),
        "username": claims.get("preferred_username"),
        "email": claims.get("email"),
        "roles": roles,
        "claims": claims,
    }


def require_roles(required: Set[str]):
    async def _role_guard(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_roles = set(user.get("roles", []))
        if not required.intersection(user_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return _role_guard


__all__ = ["get_current_user", "require_roles", "get_db_session"]
