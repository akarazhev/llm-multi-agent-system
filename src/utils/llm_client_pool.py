"""
Connection pool manager for LLM API clients.
Provides connection reuse, health checking, and graceful degradation.
"""
import asyncio
import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from openai import AsyncOpenAI
import os

logger = logging.getLogger(__name__)


class LLMClientPool:
    """
    Singleton connection pool for LLM API clients.
    Manages client lifecycle, connection reuse, and health monitoring.
    """
    
    _instance: Optional['LLMClientPool'] = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.clients: Dict[str, AsyncOpenAI] = {}
        self.client_health: Dict[str, Dict[str, Any]] = {}
        self.health_check_interval = 300  # 5 minutes
        self._initialized = True
        
        logger.info("LLM Client Pool initialized")
    
    async def get_client(
        self,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 300.0
    ) -> AsyncOpenAI:
        """
        Get or create an LLM API client.
        
        Args:
            api_base: API base URL (defaults to env var)
            api_key: API key (defaults to env var)
            timeout: Request timeout in seconds
        
        Returns:
            Configured AsyncOpenAI client
        """
        api_base = api_base or os.getenv('OPENAI_API_BASE', 'http://127.0.0.1:8080/v1')
        api_key = api_key or os.getenv('OPENAI_API_KEY', 'not-needed')
        
        # Create cache key
        cache_key = f"{api_base}:{api_key[:10] if api_key else 'none'}"
        
        # Check if client exists and is healthy
        if cache_key in self.clients:
            if await self._is_client_healthy(cache_key):
                logger.debug(f"Reusing existing client for {api_base}")
                return self.clients[cache_key]
            else:
                logger.warning(f"Removing unhealthy client for {api_base}")
                await self._remove_client(cache_key)
        
        # Create new client
        async with self._lock:
            # Double-check after acquiring lock
            if cache_key in self.clients:
                return self.clients[cache_key]
            
            logger.info(f"Creating new LLM client for {api_base}")
            client = AsyncOpenAI(
                base_url=api_base,
                api_key=api_key,
                timeout=timeout,
                max_retries=0  # We handle retries at a higher level
            )
            
            self.clients[cache_key] = client
            self.client_health[cache_key] = {
                'created_at': datetime.now(),
                'last_check': datetime.now(),
                'last_success': datetime.now(),
                'failure_count': 0,
                'request_count': 0,
                'success_count': 0
            }
            
            return client
    
    async def _is_client_healthy(self, cache_key: str) -> bool:
        """Check if a client is healthy and should be reused"""
        if cache_key not in self.client_health:
            return False
        
        health = self.client_health[cache_key]
        now = datetime.now()
        
        # Check if too many recent failures
        if health['failure_count'] >= 5:
            last_success_age = (now - health['last_success']).total_seconds()
            if last_success_age < 60:  # Recent failures
                return False
        
        # Check if client is too old (recreate every hour)
        client_age = (now - health['created_at']).total_seconds()
        if client_age > 3600:
            logger.info(f"Client {cache_key} is too old ({client_age}s), will recreate")
            return False
        
        return True
    
    async def _remove_client(self, cache_key: str):
        """Remove and close a client"""
        if cache_key in self.clients:
            try:
                # AsyncOpenAI client doesn't need explicit closing in recent versions
                # but we'll remove it from the pool
                del self.clients[cache_key]
            except Exception as e:
                logger.warning(f"Error removing client: {e}")
        
        if cache_key in self.client_health:
            del self.client_health[cache_key]
    
    def record_request(self, cache_key: str, success: bool):
        """Record request statistics for health monitoring"""
        if cache_key in self.client_health:
            health = self.client_health[cache_key]
            health['request_count'] += 1
            
            if success:
                health['success_count'] += 1
                health['last_success'] = datetime.now()
                health['failure_count'] = max(0, health['failure_count'] - 1)  # Decay failures
            else:
                health['failure_count'] += 1
    
    async def health_check(self):
        """Periodic health check to clean up unhealthy clients"""
        while True:
            try:
                await asyncio.sleep(self.health_check_interval)
                
                logger.debug("Running client pool health check")
                clients_to_remove = []
                
                for cache_key in list(self.clients.keys()):
                    if not await self._is_client_healthy(cache_key):
                        clients_to_remove.append(cache_key)
                
                for cache_key in clients_to_remove:
                    logger.info(f"Removing unhealthy client: {cache_key}")
                    await self._remove_client(cache_key)
                
                logger.debug(f"Health check complete. Active clients: {len(self.clients)}")
                
            except Exception as e:
                logger.error(f"Error in health check: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics"""
        total_requests = sum(h['request_count'] for h in self.client_health.values())
        total_successes = sum(h['success_count'] for h in self.client_health.values())
        
        return {
            'active_clients': len(self.clients),
            'total_requests': total_requests,
            'total_successes': total_successes,
            'success_rate': total_successes / total_requests if total_requests > 0 else 0,
            'clients': {
                key: {
                    'requests': health['request_count'],
                    'successes': health['success_count'],
                    'failures': health['failure_count'],
                    'age_seconds': (datetime.now() - health['created_at']).total_seconds()
                }
                for key, health in self.client_health.items()
            }
        }
    
    async def close_all(self):
        """Close all clients and clean up pool"""
        logger.info("Closing all LLM clients in pool")
        async with self._lock:
            for cache_key in list(self.clients.keys()):
                await self._remove_client(cache_key)
        logger.info("All LLM clients closed")


# Global instance
_client_pool = LLMClientPool()


async def get_llm_client(
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: float = 300.0
) -> AsyncOpenAI:
    """
    Get an LLM API client from the pool.
    
    Args:
        api_base: API base URL (defaults to env var)
        api_key: API key (defaults to env var)
        timeout: Request timeout in seconds
    
    Returns:
        Configured AsyncOpenAI client
    """
    return await _client_pool.get_client(api_base, api_key, timeout)


def get_pool_stats() -> Dict[str, Any]:
    """Get statistics about the client pool"""
    return _client_pool.get_stats()


async def close_client_pool():
    """Close the client pool and all connections"""
    await _client_pool.close_all()
