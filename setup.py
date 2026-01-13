#!/usr/bin/env python3
"""
Setup script for LLM Multi-Agent System with Cursor CLI Orchestration
"""
import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def check_python_version():
    print("Checking Python version...")
    if sys.version_info < (3, 12):
        print(f"❌ Python 3.12 required. Current version: {sys.version}")
        print(f"   Install with: brew install python@3.12")
        return False
    if sys.version_info >= (3, 13):
        print(f"⚠️  Warning: Python {sys.version_info.major}.{sys.version_info.minor} detected")
        print(f"   Python 3.12 is recommended. Newer versions may have compatibility issues.")
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_llama_server():
    print("\nChecking local llama-server...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8080))
        sock.close()
        if result == 0:
            print("✓ llama-server is running on port 8080")
            return True
        else:
            print("⚠️  llama-server is not running")
            print("   Start it with: ./scripts/start_llama_server.sh")
            return False
    except Exception as e:
        print(f"⚠️  Error checking llama-server: {e}")
        return False


def create_directories():
    print("\nCreating necessary directories...")
    dirs = ["output", "logs"]
    for dir_name in dirs:
        path = Path(dir_name)
        path.mkdir(exist_ok=True)
        print(f"✓ Created {dir_name}/")


def install_dependencies():
    print("\nInstalling Python dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def setup_config():
    print("\nSetting up configuration...")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("✓ Created .env file from template")
    else:
        print("✓ .env file already exists")
    
    config_file = Path("config.yaml")
    if config_file.exists():
        print("✓ config.yaml exists")
        
        workspace = os.getcwd()
        print(f"\n   Current workspace: {workspace}")
        print("   Update cursor_workspace in config.yaml if needed")
    else:
        print("⚠️  config.yaml not found")


def run_verification():
    print("\nRunning verification...")
    try:
        result = subprocess.run(
            [sys.executable, "-c", "from src.orchestrator import AgentOrchestrator; print('✓ Import successful')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print("❌ Import verification failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False


def print_next_steps():
    print_header("Setup Complete!")
    
    print("Next steps:")
    print("\n1. Update configuration (if needed):")
    print("   - Edit config.yaml to set your workspace path")
    print("   - Adjust agent settings and timeouts")
    
    print("\n2. Run the system:")
    print("   python main.py")
    
    print("\n3. Or try an example:")
    print("   python examples/simple_workflow.py")
    
    print("\n4. Read the documentation:")
    print("   - Quick Start: docs/QUICK_START.md")
    print("   - START_HERE Guide: docs/START_HERE.md")
    print("   - LangGraph Integration: docs/INTEGRATIONS.md")
    
    print("\n" + "="*80 + "\n")


def main():
    print_header("LLM Multi-Agent System Setup")
    
    print("This script will set up the multi-agent system on your machine.\n")
    
    checks_passed = True
    
    if not check_python_version():
        checks_passed = False
    
    llama_ok = check_llama_server()
    if not llama_ok:
        print("\n⚠️  Warning: llama-server not running.")
        print("   You can start it later with: ./scripts/start_llama_server.sh")
        print("   Continuing with setup...")
    
    if not checks_passed:
        print("\n❌ Prerequisites not met. Please fix the issues above and try again.")
        return 1
    
    create_directories()
    
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation.")
        return 1
    
    setup_config()
    
    if not run_verification():
        print("\n⚠️  Verification failed, but setup may still work.")
        print("   Try running: python main.py")
    
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
