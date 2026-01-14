"""
Retry utilities for production-ready error handling with exponential backoff.
"""
import asyncio
import logging
from typing import TypeVar, Callable, Optional, Type, Tuple
from functools import wraps
import random

logger = logging.getLogger(__name__)

T = TypeVar('T')


class RetryError(Exception):
    """Raised when all retry attempts have been exhausted"""
    pass


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open"""
    pass


class CircuitBreaker:
    """
    Circuit breaker implementation to prevent cascade failures.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, requests fail immediately
    - HALF_OPEN: Testing if service recovered, limited requests pass through
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_attempts: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_attempts = half_open_attempts
        
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.half_open_success_count = 0
    
    def call(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator to protect a function with circuit breaker"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                # Check if recovery timeout has passed
                if self.last_failure_time and (
                    asyncio.get_event_loop().time() - self.last_failure_time >= self.recovery_timeout
                ):
                    logger.info("Circuit breaker entering HALF_OPEN state")
                    self.state = "HALF_OPEN"
                    self.half_open_success_count = 0
                else:
                    raise CircuitBreakerError("Circuit breaker is OPEN")
            
            try:
                result = await func(*args, **kwargs)
                
                # Success - handle state transitions
                if self.state == "HALF_OPEN":
                    self.half_open_success_count += 1
                    if self.half_open_success_count >= self.half_open_attempts:
                        logger.info("Circuit breaker CLOSED after successful recovery")
                        self.state = "CLOSED"
                        self.failure_count = 0
                elif self.state == "CLOSED":
                    # Reset failure count on success
                    if self.failure_count > 0:
                        self.failure_count = 0
                
                return result
                
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = asyncio.get_event_loop().time()
                
                if self.state == "HALF_OPEN":
                    logger.warning("Circuit breaker opening due to failure in HALF_OPEN state")
                    self.state = "OPEN"
                elif self.failure_count >= self.failure_threshold:
                    logger.warning(f"Circuit breaker opening after {self.failure_count} failures")
                    self.state = "OPEN"
                
                raise
        
        return wrapper


async def retry_with_exponential_backoff(
    func: Callable[..., T],
    *args,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retriable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    non_retriable_exceptions: Tuple[Type[Exception], ...] = (),
    **kwargs
) -> T:
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Async function to retry
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff (typically 2)
        jitter: Add random jitter to prevent thundering herd
        retriable_exceptions: Exceptions that should trigger a retry
        non_retriable_exceptions: Exceptions that should not be retried
        *args, **kwargs: Arguments to pass to the function
    
    Returns:
        Result of the function call
    
    Raises:
        RetryError: If all attempts failed
        Exception: If non-retriable exception occurred
    """
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            result = await func(*args, **kwargs)
            if attempt > 0:
                logger.info(f"Function succeeded on attempt {attempt + 1}")
            return result
            
        except non_retriable_exceptions as e:
            logger.error(f"Non-retriable exception occurred: {e}")
            raise
            
        except retriable_exceptions as e:
            last_exception = e
            
            if attempt < max_attempts - 1:
                # Calculate delay with exponential backoff
                delay = min(initial_delay * (exponential_base ** attempt), max_delay)
                
                # Add jitter to prevent thundering herd
                if jitter:
                    delay = delay * (0.5 + random.random())
                
                logger.warning(
                    f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                    f"Retrying in {delay:.2f}s..."
                )
                
                await asyncio.sleep(delay)
            else:
                logger.error(f"All {max_attempts} attempts failed")
    
    raise RetryError(f"Failed after {max_attempts} attempts: {last_exception}")


def retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retriable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    non_retriable_exceptions: Tuple[Type[Exception], ...] = ()
):
    """
    Decorator for retrying async functions with exponential backoff.
    
    Example:
        @retry(max_attempts=3, initial_delay=1.0)
        async def fetch_data():
            return await api_call()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await retry_with_exponential_backoff(
                func,
                *args,
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                max_delay=max_delay,
                exponential_base=exponential_base,
                jitter=jitter,
                retriable_exceptions=retriable_exceptions,
                non_retriable_exceptions=non_retriable_exceptions,
                **kwargs
            )
        return wrapper
    return decorator
