"""
Token Bucket Rate Limiter

This module implements a Token Bucket Algorithm for rate limiting HTTP requests
or any other operations that need to be rate-limited.

The Token Bucket Algorithm works by:
1. A bucket holds a maximum number of tokens
2. Tokens are added to the bucket at a fixed rate (refill rate)
3. Each operation consumes one or more tokens
4. If there aren't enough tokens, the operation is rejected or delayed
"""

import time
import threading
from dataclasses import dataclass
from enum import Enum


class RateLimitStrategy(Enum):
    """Strategy for handling rate limit violations."""
    REJECT = "reject"  # Reject the request immediately
    WAIT = "wait"      # Wait until tokens are available


@dataclass
class RateLimitConfig:
    """Configuration for the rate limiter."""
    capacity: int          # Maximum number of tokens in the bucket
    refill_rate: float     # Tokens added per second
    strategy: RateLimitStrategy = RateLimitStrategy.REJECT
    max_wait_time: float = 30.0  # Maximum time to wait when strategy is WAIT


class TokenBucketRateLimiter:
    """
    Token Bucket Rate Limiter implementation.
    
    This rate limiter uses the token bucket algorithm to control the rate
    of operations. It's thread-safe and can be used in concurrent environments.
    
    Example:
        # Allow 10 requests per second, with a burst capacity of 20
        limiter = TokenBucketRateLimiter(
            capacity=20,
            refill_rate=10.0,
            strategy=RateLimitStrategy.REJECT
        )
        
        # Check if request is allowed
        if limiter.acquire():
            # Make the request
            make_api_call()
        else:
            # Handle rate limit
            print("Rate limited")
    """
    
    def __init__(self, config: RateLimitConfig):
        """
        Initialize the rate limiter.
        
        Args:
            config: Rate limiter configuration
        """
        self.config = config
        self.tokens = float(config.capacity)  # Start with full bucket
        self.last_refill = time.time()
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    @classmethod
    def create(
        self,
        capacity: int,
        refill_rate: float,
        strategy: RateLimitStrategy = RateLimitStrategy.REJECT,
        max_wait_time: float = 30.0
    ) -> "TokenBucketRateLimiter":
        """
        Create a rate limiter with the given parameters.
        
        Args:
            capacity: Maximum number of tokens in the bucket
            refill_rate: Tokens added per second
            strategy: How to handle rate limit violations
            max_wait_time: Maximum time to wait when strategy is WAIT
            
        Returns:
            TokenBucketRateLimiter instance
        """
        config = RateLimitConfig(
            capacity=capacity,
            refill_rate=refill_rate,
            strategy=strategy,
            max_wait_time=max_wait_time
        )
        return TokenBucketRateLimiter(config)
    
    def refill_tokens(self) -> None:
        """Refill tokens based on elapsed time since last refill."""
        now = time.time()
        elapsed = now - self.last_refill
        
        # Calculate how many tokens to add
        tokens_to_add = elapsed * self.config.refill_rate
        
        # Add tokens but don't exceed capacity
        self.tokens = min(self.config.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def acquire(self, tokens: int = 1, timeout: float | None = None) -> bool:
        """
        Attempt to acquire the specified number of tokens.
        
        Args:
            tokens: Number of tokens to acquire (default: 1)
            timeout: Maximum time to wait (overrides config.max_wait_time)
            
        Returns:
            True if tokens were successfully acquired, False otherwise
            
        Raises:
            ValueError: If tokens <= 0 or tokens > capacity
        """
        if tokens <= 0:
            raise ValueError("Number of tokens must be positive")
        
        if tokens > self.config.capacity:
            raise ValueError(f"Requested tokens ({tokens}) exceeds bucket capacity ({self.config.capacity})")
        
        with self._lock:
            self.refill_tokens()
            
            # If we have enough tokens, consume them immediately
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            # Not enough tokens - handle based on strategy
            if self.config.strategy == RateLimitStrategy.REJECT:
                return False
            
            # WAIT strategy - calculate wait time
            tokens_needed = tokens - self.tokens
            wait_time = tokens_needed / self.config.refill_rate
            
            # Use provided timeout or config max_wait_time
            max_wait = timeout if timeout is not None else self.config.max_wait_time
            
            if wait_time > max_wait:
                return False
            
            # Wait for tokens to be available
            time.sleep(wait_time)
            
            # Refill and try again
            self.refill_tokens()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False
    
    def try_acquire(self, tokens: int = 1) -> bool:
        """
        Try to acquire tokens without waiting (always uses REJECT strategy).
        
        Args:
            tokens: Number of tokens to acquire
            
        Returns:
            True if tokens were successfully acquired, False otherwise
        """
        with self._lock:
            self.refill_tokens()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False
    
    def get_available_tokens(self) -> float:
        """
        Get the current number of available tokens.
        
        Returns:
            Current number of tokens in the bucket
        """
        with self._lock:
            self.refill_tokens()
            return self.tokens
    
    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait for the specified number of tokens.
        
        Args:
            tokens: Number of tokens needed
            
        Returns:
            Time in seconds to wait for tokens (0 if tokens are available)
        """
        with self._lock:
            self.refill_tokens()
            
            if self.tokens >= tokens:
                return 0.0
            
            tokens_needed = tokens - self.tokens
            return tokens_needed / self.config.refill_rate
    
    def reset(self) -> None:
        """Reset the bucket to full capacity."""
        with self._lock:
            self.tokens = float(self.config.capacity)
            self.last_refill = time.time()
    
    def __str__(self) -> str:
        """String representation of the rate limiter."""
        return (
            f"TokenBucketRateLimiter("
            f"capacity={self.config.capacity}, "
            f"refill_rate={self.config.refill_rate}, "
            f"strategy={self.config.strategy.value}, "
            f"available_tokens={self.get_available_tokens():.2f})"
        )
    
    def __repr__(self) -> str:
        """Detailed representation of the rate limiter."""
        return self.__str__()


class RateLimitedHTTPClient:
    """
    HTTP client wrapper with built-in rate limiting.
    
    This class wraps an httpx.Client and applies rate limiting to all requests.
    """
    
    def __init__(
        self,
        rate_limiter: TokenBucketRateLimiter,
        client: object = None
    ):
        """
        Initialize the rate-limited HTTP client.
        
        Args:
            rate_limiter: TokenBucketRateLimiter instance
            client: Optional httpx client (will create one if not provided)
        """
        self.rate_limiter = rate_limiter
        
        if client is None:
            import httpx
            self.client = httpx.Client()
            self._owns_client = True
        else:
            self.client = client
            self._owns_client = False
    
    def request(self, method: str, url: str, **kwargs):
        """
        Make a rate-limited HTTP request.
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional arguments passed to httpx
            
        Returns:
            httpx.Response if successful
            
        Raises:
            RateLimitException: If rate limit is exceeded and strategy is REJECT
        """
        if not self.rate_limiter.acquire():
            raise RateLimitException("Rate limit exceeded")
        
        return self.client.request(method, url, **kwargs)
    
    def get(self, url: str, **kwargs):
        """Make a rate-limited GET request."""
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs):
        """Make a rate-limited POST request."""
        return self.request("POST", url, **kwargs)
    
    def put(self, url: str, **kwargs):
        """Make a rate-limited PUT request."""
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url: str, **kwargs):
        """Make a rate-limited DELETE request."""
        return self.request("DELETE", url, **kwargs)
    
    def close(self):
        """Close the HTTP client if we own it."""
        if self._owns_client and hasattr(self.client, 'close'):
            self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class RateLimitException(Exception):
    """Exception raised when rate limit is exceeded."""
    pass

# Decorator for rate-limiting functions
def rate_limited(
    capacity: int,
    refill_rate: float,
    strategy: RateLimitStrategy = RateLimitStrategy.REJECT,
    max_wait_time: float = 30.0
):
    """
    Decorator to add rate limiting to a function.
    
    Args:
        capacity: Maximum number of tokens
        refill_rate: Tokens per second
        strategy: Rate limit strategy
        max_wait_time: Maximum wait time
        
    Example:
        @rate_limited(capacity=10, refill_rate=1.0)
        def api_call():
            # This function will be rate limited
            pass
    """
    config = RateLimitConfig(
        capacity=capacity,
        refill_rate=refill_rate,
        strategy=strategy,
        max_wait_time=max_wait_time
    )
    limiter = TokenBucketRateLimiter(config)
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not limiter.acquire():
                raise RateLimitException(f"Rate limit exceeded for function {func.__name__}")
            return func(*args, **kwargs)
        
        wrapper.rate_limiter = limiter
        return wrapper
    
    return decorator


def create_rate_limiter_from_env() -> TokenBucketRateLimiter:
    """
    Create a rate limiter using configuration from environment variables.
    
    Environment variables:
        RATE_LIMITER_CAPACITY: Token bucket capacity (default: 20)
        RATE_LIMITER_REFILL_RATE: Tokens per second (default: 10)
        RATE_LIMITER_STRATEGY: REJECT or WAIT (default: REJECT)
        RATE_LIMITER_MAX_WAIT_TIME: Max wait time in seconds (default: 30)
    
    Returns:
        TokenBucketRateLimiter configured from environment variables
    """
    import os
    
    # Try to load .env file if python-dotenv is available
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except ImportError:
        # python-dotenv not available, just use os.environ
        pass
    
    # Get configuration from environment variables with defaults
    try:
        capacity = int(os.getenv('RATE_LIMITER_CAPACITY', '20'))
    except ValueError:
        print("Warning: Invalid RATE_LIMITER_CAPACITY value, using default (20)")
        capacity = 20
    
    try:
        refill_rate = float(os.getenv('RATE_LIMITER_REFILL_RATE', '10'))
    except ValueError:
        print("Warning: Invalid RATE_LIMITER_REFILL_RATE value, using default (10)")
        refill_rate = 10.0
    
    strategy_str = os.getenv('RATE_LIMITER_STRATEGY', 'REJECT').upper()
    if strategy_str == 'WAIT':
        strategy = RateLimitStrategy.WAIT
    else:
        strategy = RateLimitStrategy.REJECT
    
    try:
        max_wait_time = float(os.getenv('RATE_LIMITER_MAX_WAIT_TIME', '30'))
    except ValueError:
        print("Warning: Invalid RATE_LIMITER_MAX_WAIT_TIME value, using default (30)")
        max_wait_time = 30.0
    
    rate_config = RateLimitConfig(
        capacity=capacity,
        refill_rate=refill_rate,
        strategy=strategy,
        max_wait_time=max_wait_time
    )
    
    return TokenBucketRateLimiter(rate_config)
