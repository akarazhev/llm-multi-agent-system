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


def check_cursor_cli():
    print("\nChecking Cursor CLI installation...")
    try:
        result = subprocess.run(
            ["cursor", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Cursor CLI is installed and accessible")
            return True
        else:
            print("⚠️  Cursor CLI found but may not be working correctly")
            return False
    except FileNotFoundError:
        print("❌ Cursor CLI not found in PATH")
        print("   Please install Cursor IDE from https://cursor.sh")
        print("   Or specify the full path in config.yaml")
        return False
    except Exception as e:
        print(f"⚠️  Error checking Cursor CLI: {e}")
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
    print("   - Full Guide: docs/CURSOR_CLI_ORCHESTRATION.md")
    
    print("\n" + "="*80 + "\n")


def main():
    print_header("LLM Multi-Agent System Setup")
    
    print("This script will set up the multi-agent system on your machine.\n")
    
    checks_passed = True
    
    if not check_python_version():
        checks_passed = False
    
    cursor_ok = check_cursor_cli()
    if not cursor_ok:
        print("\n⚠️  Warning: Cursor CLI not found or not working.")
        print("   The system will not work without Cursor CLI.")
        response = input("\n   Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("\nSetup cancelled.")
            return 1
    
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
