#!/usr/bin/env python3
"""
Quick test to demonstrate improved progress tracking
"""

import asyncio
from src.utils.chat_display import AgentChatDisplay, ProgressTracker

async def test_progress_tracking():
    """Demonstrate the improved progress tracking"""
    
    chat = AgentChatDisplay()
    tracker = ProgressTracker(total_steps=6)
    
    chat.print_header("Progress Tracking Improvement Demo")
    
    print("\n" + "="*80)
    print("Simulating Feature Development Workflow")
    print("="*80 + "\n")
    
    # Step 1: Business Analyst
    chat.agent_message("business_analyst", "Analyzing requirements...", "thinking")
    await asyncio.sleep(1)
    tracker.update_with_count(["business_analyst"])
    chat.agent_completed("business_analyst", "Requirements complete", ["requirements.md"])
    
    await asyncio.sleep(1)
    
    # Step 2: Architecture Design
    chat.inter_agent_communication("business_analyst", "developer", "Requirements ready")
    chat.agent_message("developer", "Designing architecture...", "thinking")
    await asyncio.sleep(1)
    tracker.update_with_count(["business_analyst", "architecture_design"])
    chat.agent_completed("developer", "Architecture complete", ["design.md"])
    
    await asyncio.sleep(1)
    
    # Step 3: Implementation
    chat.agent_message("developer", "Implementing features...", "working")
    await asyncio.sleep(1)
    tracker.update_with_count(["business_analyst", "architecture_design", "implementation"])
    chat.agent_completed("developer", "Implementation complete", ["app.py", "models.py"])
    
    await asyncio.sleep(1)
    
    # Steps 4 & 5: Parallel Execution
    chat.parallel_execution_start(["qa_engineer", "devops_engineer"])
    
    await asyncio.sleep(0.5)
    
    # QA starts
    chat.agent_message("qa_engineer", "Creating test suite...", "thinking")
    await asyncio.sleep(1)
    
    # DevOps starts (parallel)
    chat.agent_message("devops_engineer", "Setting up infrastructure...", "thinking")
    await asyncio.sleep(1)
    
    # QA completes
    tracker.update_with_count(["business_analyst", "architecture_design", "implementation", "qa_testing"])
    chat.agent_completed("qa_engineer", "Tests complete", ["test_app.py"])
    
    await asyncio.sleep(0.5)
    
    # DevOps completes
    tracker.update_with_count(["business_analyst", "architecture_design", "implementation", "qa_testing", "infrastructure"])
    chat.agent_completed("devops_engineer", "Infrastructure ready", ["Dockerfile"])
    
    await asyncio.sleep(0.5)
    
    chat.parallel_execution_complete(["qa_engineer", "devops_engineer"])
    
    await asyncio.sleep(1)
    
    # Step 6: Documentation
    chat.inter_agent_communication("system", "technical_writer", "Ready for docs")
    chat.agent_message("technical_writer", "Writing documentation...", "thinking")
    await asyncio.sleep(1)
    tracker.update_with_count(["business_analyst", "architecture_design", "implementation", "qa_testing", "infrastructure", "documentation"])
    chat.agent_completed("technical_writer", "Documentation complete", ["README.md"])
    
    print("\n" + "="*80)
    print("✨ Workflow Complete!")
    print("="*80 + "\n")
    
    # Show workflow status
    chat.workflow_status(
        "demo_workflow_001",
        "completed",
        "documentation",
        ["business_analyst", "architecture_design", "implementation", "qa_testing", "infrastructure", "documentation"]
    )
    
    chat.conversation_summary()

if __name__ == "__main__":
    print("\n🚀 Testing improved progress tracking...")
    print("Watch how progress updates step-by-step!\n")
    asyncio.run(test_progress_tracking())
    print("\n✅ Test complete! This is how your workflows will look now.\n")
