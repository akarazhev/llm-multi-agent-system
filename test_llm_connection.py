#!/usr/bin/env python3
"""
Test script to verify LLM connection and configuration.
This script checks if the project can connect to the LLM server.
"""
import asyncio
import os
import sys
from pathlib import Path

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    PROJECT_ROOT = Path(__file__).parent.absolute()
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

# Add project to path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.utils.llm_client_pool import get_llm_client
except ImportError as e:
    print(f"Error importing LLM client: {e}")
    print("Please ensure dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


async def test_llm_connection():
    """Test LLM connection and configuration"""
    print("="*80)
    print("LLM Connection Test")
    print("="*80)
    print()
    
    # Check environment variables
    print("1. Checking Environment Variables:")
    print("-" * 80)
    api_base = os.getenv('OPENAI_API_BASE', 'http://127.0.0.1:8080/v1')
    api_key = os.getenv('OPENAI_API_KEY', 'not-needed')
    api_model = os.getenv('OPENAI_API_MODEL', 'devstral')
    
    print(f"   OPENAI_API_BASE: {api_base}")
    if api_key and api_key != 'not-needed':
        print(f"   OPENAI_API_KEY: {'*' * min(len(api_key), 10)}...")
    else:
        print(f"   OPENAI_API_KEY: {api_key} (default)")
    print(f"   OPENAI_API_MODEL: {api_model}")
    
    print()
    
    # Test connection
    print("2. Testing LLM Connection:")
    print("-" * 80)
    try:
        print(f"   → Creating client for: {api_base}")
        client = await get_llm_client(
            api_base=api_base,
            api_key=api_key,
            timeout=10.0  # Short timeout for test
        )
        print(f"   ✓ Client created successfully")
        
        # Try a simple API call
        print(f"   → Sending test request to model '{api_model}'...")
        
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=api_model,
                messages=[
                    {"role": "user", "content": "Say 'Hello, connection test successful!' and nothing else."}
                ],
                max_tokens=50,
                temperature=0.1
            ),
            timeout=30.0
        )
        
        if response and response.choices:
            content = response.choices[0].message.content
            print(f"   ✓ Response received successfully!")
            print(f"   ✓ Response: {content.strip()}")
            print()
            print("="*80)
            print("✓ SUCCESS: LLM connection is working!")
            print("="*80)
            return True
        else:
            print(f"   ✗ No response content received")
            return False
            
    except asyncio.TimeoutError:
        print(f"   ✗ Connection timeout (server may be slow or not responding)")
        print()
        print("="*80)
        print("✗ FAILED: Connection timeout")
        print("="*80)
        print("\nTroubleshooting:")
        print("  - Check if your LLM server is running")
        print(f"  - Verify the server is accessible at: {api_base}")
        print("  - Try: curl http://127.0.0.1:8080/health")
        return False
        
    except ConnectionError as e:
        print(f"   ✗ Connection error: {e}")
        print()
        print("="*80)
        print("✗ FAILED: Connection error")
        print("="*80)
        print("\nTroubleshooting:")
        print("  - Ensure your LLM server is running")
        print(f"  - Check if the server is accessible at: {api_base}")
        print("  - Verify network connectivity")
        print(f"  - Error details: {e}")
        return False
        
    except Exception as e:
        print(f"   ✗ Error: {type(e).__name__}: {e}")
        print()
        print("="*80)
        print("✗ FAILED: Unexpected error")
        print("="*80)
        print(f"\nError details: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(test_llm_connection())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
