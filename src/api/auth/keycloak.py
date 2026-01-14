import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Set

import httpx
from jose import jwt

from src.config import load_config


@dataclass
class KeycloakSettings:
    server_url: str
    realm: str
    client_id: str
    audience: Optional[str] = None

    @property
    def issuer(self) -> str:
        return f"{self.server_url}/realms/{self.realm}"

    @property
    def jwks_url(self) -> str:
        return f"{self.issuer}/protocol/openid-connect/certs"


class KeycloakJwksCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl_seconds = ttl_seconds
        self.cached_at = 0.0
        self.jwks: Dict[str, Any] = {}

    async def get_jwks(self, settings: KeycloakSettings) -> Dict[str, Any]:
        now = time.time()
        if self.jwks and (now - self.cached_at) < self.ttl_seconds:
            return self.jwks
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(settings.jwks_url)
            response.raise_for_status()
            self.jwks = response.json()
            self.cached_at = now
            return self.jwks


JWKS_CACHE = KeycloakJwksCache()


def load_keycloak_settings() -> KeycloakSettings:
    config = load_config()
    raw = config.keycloak or {}
    server_url = raw.get("server_url", "http://localhost:8081")
    realm = raw.get("realm", "llm-agents")
    client_id = raw.get("client_id", "llm-agent-ui")
    audience = raw.get("audience")
    return KeycloakSettings(server_url=server_url, realm=realm, client_id=client_id, audience=audience)


def extract_roles(payload: Dict[str, Any], client_id: str) -> Set[str]:
    roles: Set[str] = set()
    realm_access = payload.get("realm_access", {}).get("roles", [])
    roles.update(realm_access)
    resource_access = payload.get("resource_access", {}).get(client_id, {})
    roles.update(resource_access.get("roles", []))
    return roles


async def decode_token(token: str) -> Dict[str, Any]:
    settings = load_keycloak_settings()
    jwks = await JWKS_CACHE.get_jwks(settings)
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    if not kid:
        raise ValueError("Token header missing kid")
    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        raise ValueError("Signing key not found")

    claims = jwt.decode(
        token,
        key,
        algorithms=[headers.get("alg", "RS256")],
        issuer=settings.issuer,
        audience=settings.audience or settings.client_id,
        options={"verify_aud": settings.audience is not None},
    )
    return claims
