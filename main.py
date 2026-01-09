"""
Main entry point for the LLM Multi-Agent System.

Run with: python main.py
Or with uvicorn: uvicorn main:app --reload
"""

import uvicorn

from src.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
