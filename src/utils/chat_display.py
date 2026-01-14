"""
Interactive Chat Display Utility for Multi-Agent Communication

This module provides rich, interactive chat-like display for agent communications,
making it easy to follow the flow of work between agents in real-time.
"""

import sys
from typing import Dict, Any, Optional, List
from datetime import datetime
from colorama import Fore, Back, Style, init
from pathlib import Path

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class AgentChatDisplay:
    """
    Provides rich, chat-like display for agent communications.
    Displays agent messages, actions, and status updates in an interactive format.
    """
    
    # Agent color mapping for visual distinction
    AGENT_COLORS = {
        "business_analyst": Fore.CYAN,
        "developer": Fore.GREEN,
        "qa_engineer": Fore.YELLOW,
        "devops_engineer": Fore.MAGENTA,
        "technical_writer": Fore.BLUE,
        "system": Fore.WHITE,
    }
    
    # Status icons
    ICONS = {
        "start": "🚀",
        "working": "⚙️",
        "thinking": "🤔",
        "completed": "✅",
        "error": "❌",
        "info": "ℹ️",
        "file": "📄",
        "chat": "💬",
        "question": "❓",
        "answer": "💡",
        "warning": "⚠️",
    }
    
    def __init__(self, show_timestamps: bool = True, show_agent_icons: bool = True):
        self.show_timestamps = show_timestamps
        self.show_agent_icons = show_agent_icons
        self.message_history: List[Dict[str, Any]] = []
        self._last_agent = None
    
    def _get_agent_color(self, agent_id: str) -> str:
        """Get color for agent based on their role"""
        for role_key in self.AGENT_COLORS:
            if role_key in agent_id.lower():
                return self.AGENT_COLORS[role_key]
        return Fore.WHITE
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        if self.show_timestamps:
            return f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} "
        return ""
    
    def print_header(self, title: str):
        """Print a styled header"""
        width = 80
        print("\n" + "=" * width)
        print(f"{Style.BRIGHT}{title.center(width)}{Style.RESET_ALL}")
        print("=" * width + "\n")
    
    def print_section(self, title: str):
        """Print a section header"""
        print(f"\n{Style.BRIGHT}{Fore.WHITE}{'─' * 40}")
        print(f"  {title}")
        print(f"{'─' * 40}{Style.RESET_ALL}\n")
    
    def agent_message(
        self,
        agent_id: str,
        message: str,
        message_type: str = "info",
        to_agent: Optional[str] = None
    ):
        """
        Display an agent message in chat format.
        
        Args:
            agent_id: ID of the sending agent
            message: Message content
            message_type: Type of message (info, thinking, action, etc.)
            to_agent: Optional target agent ID
        """
        color = self._get_agent_color(agent_id)
        icon = self.ICONS.get(message_type, self.ICONS["chat"])
        timestamp = self._get_timestamp()
        
        # Add spacing between different agents for better readability
        if self._last_agent and self._last_agent != agent_id:
            print()
        
        self._last_agent = agent_id
        
        # Format agent name with color
        agent_name = agent_id.replace("_", " ").title()
        
        # Show who the message is directed to
        to_text = ""
        if to_agent:
            to_color = self._get_agent_color(to_agent)
            to_name = to_agent.replace("_", " ").title()
            to_text = f" → {to_color}{Style.BRIGHT}{to_name}{Style.RESET_ALL}"
        
        # Print the message
        print(f"{timestamp}{icon} {color}{Style.BRIGHT}{agent_name}{Style.RESET_ALL}{to_text}:")
        
        # Indent the message content
        for line in message.split('\n'):
            if line.strip():
                print(f"  {color}{line}{Style.RESET_ALL}")
        
        # Store in history
        self.message_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "to_agent": to_agent,
            "message_type": message_type,
            "message": message
        })
    
    def agent_action(self, agent_id: str, action: str, details: Optional[str] = None):
        """Display an agent performing an action"""
        color = self._get_agent_color(agent_id)
        timestamp = self._get_timestamp()
        agent_name = agent_id.replace("_", " ").title()
        
        print(f"{timestamp}{self.ICONS['working']} {color}{Style.BRIGHT}{agent_name}{Style.RESET_ALL} {action}")
        
        if details:
            print(f"  {Fore.LIGHTBLACK_EX}{details}{Style.RESET_ALL}")
    
    def agent_thinking(self, agent_id: str, thought: str):
        """Display agent thinking/reasoning"""
        self.agent_message(agent_id, thought, message_type="thinking")
    
    def agent_completed(self, agent_id: str, summary: str, files_created: Optional[List[str]] = None):
        """Display agent task completion"""
        color = self._get_agent_color(agent_id)
        timestamp = self._get_timestamp()
        agent_name = agent_id.replace("_", " ").title()
        
        print(f"\n{timestamp}{self.ICONS['completed']} {color}{Style.BRIGHT}{agent_name}{Style.RESET_ALL} completed task")
        print(f"  {Fore.GREEN}{summary}{Style.RESET_ALL}")
        
        if files_created:
            print(f"  {self.ICONS['file']} Files created: {len(files_created)}")
            for file_path in files_created[:5]:  # Show first 5 files
                file_name = Path(file_path).name
                print(f"    • {Fore.LIGHTBLUE_EX}{file_name}{Style.RESET_ALL}")
            if len(files_created) > 5:
                print(f"    ... and {len(files_created) - 5} more")
    
    def agent_error(self, agent_id: str, error: str):
        """Display an agent error"""
        color = self._get_agent_color(agent_id)
        timestamp = self._get_timestamp()
        agent_name = agent_id.replace("_", " ").title()
        
        print(f"\n{timestamp}{self.ICONS['error']} {color}{Style.BRIGHT}{agent_name}{Style.RESET_ALL} encountered an error")
        print(f"  {Fore.RED}{error}{Style.RESET_ALL}")
    
    def workflow_status(self, workflow_id: str, status: str, step: str, completed_steps: List[str]):
        """Display overall workflow status"""
        timestamp = self._get_timestamp()
        
        status_color = Fore.GREEN if status == "running" else Fore.YELLOW
        
        # Count unique completed steps
        unique_steps = set(completed_steps) if completed_steps else set()
        steps_count = len(unique_steps)
        
        print(f"\n{timestamp}{self.ICONS['info']} {Style.BRIGHT}Workflow Status{Style.RESET_ALL}")
        print(f"  ID: {Fore.LIGHTBLACK_EX}{workflow_id}{Style.RESET_ALL}")
        print(f"  Status: {status_color}{status}{Style.RESET_ALL}")
        print(f"  Current Step: {Fore.CYAN}{step}{Style.RESET_ALL}")
        print(f"  Progress: {steps_count} steps completed")
        
        # Show progress bar based on unique steps
        total_steps = 6  # Typical workflow steps
        progress = min(steps_count, total_steps)
        bar_length = 30
        filled = int((progress / total_steps) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        percentage = int((progress / total_steps) * 100)
        
        print(f"  {Fore.CYAN}{bar}{Style.RESET_ALL} {percentage}%")
        
        # Show which steps are completed
        if unique_steps:
            completed_list = ", ".join(sorted(unique_steps))
            print(f"  {Fore.LIGHTBLACK_EX}Completed: {completed_list}{Style.RESET_ALL}")
    
    def inter_agent_communication(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        communication_type: str = "handoff"
    ):
        """Display communication between agents"""
        from_color = self._get_agent_color(from_agent)
        to_color = self._get_agent_color(to_agent)
        timestamp = self._get_timestamp()
        
        from_name = from_agent.replace("_", " ").title()
        to_name = to_agent.replace("_", " ").title()
        
        icon = "🔄" if communication_type == "handoff" else self.ICONS["chat"]
        
        print(f"\n{timestamp}{icon} {from_color}{Style.BRIGHT}{from_name}{Style.RESET_ALL} "
              f"→ {to_color}{Style.BRIGHT}{to_name}{Style.RESET_ALL}")
        print(f"  {Fore.LIGHTYELLOW_EX}{message}{Style.RESET_ALL}")
    
    def system_message(self, message: str, message_type: str = "info"):
        """Display a system message"""
        timestamp = self._get_timestamp()
        icon = self.ICONS.get(message_type, self.ICONS["info"])
        
        print(f"\n{timestamp}{icon} {Style.BRIGHT}System:{Style.RESET_ALL} {message}")
    
    def parallel_execution_start(self, agents: List[str]):
        """Display start of parallel execution"""
        timestamp = self._get_timestamp()
        agents_str = " & ".join([a.replace("_", " ").title() for a in agents])
        
        print(f"\n{timestamp}⚡ {Style.BRIGHT}Parallel Execution:{Style.RESET_ALL} {Fore.YELLOW}{agents_str}{Style.RESET_ALL}")
        print(f"  {Fore.LIGHTBLACK_EX}These agents will work simultaneously{Style.RESET_ALL}")
    
    def parallel_execution_complete(self, agents: List[str]):
        """Display completion of parallel execution"""
        timestamp = self._get_timestamp()
        agents_str = " & ".join([a.replace("_", " ").title() for a in agents])
        
        print(f"\n{timestamp}✅ {Style.BRIGHT}Parallel Complete:{Style.RESET_ALL} {Fore.GREEN}{agents_str}{Style.RESET_ALL}")
        print(f"  {Fore.LIGHTBLACK_EX}All parallel tasks finished{Style.RESET_ALL}")
    
    def file_operation(self, agent_id: str, operation: str, file_path: str, success: bool = True):
        """Display file operations"""
        color = self._get_agent_color(agent_id)
        timestamp = self._get_timestamp()
        agent_name = agent_id.replace("_", " ").title()
        
        status_icon = self.ICONS["completed"] if success else self.ICONS["error"]
        file_name = Path(file_path).name
        
        print(f"{timestamp}{status_icon} {color}{agent_name}{Style.RESET_ALL} {operation}: "
              f"{Fore.LIGHTBLUE_EX}{file_name}{Style.RESET_ALL}")
    
    def conversation_summary(self):
        """Display a summary of the conversation"""
        if not self.message_history:
            return
        
        self.print_section("Conversation Summary")
        
        # Count messages per agent
        agent_counts = {}
        for msg in self.message_history:
            agent_id = msg["agent_id"]
            agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1
        
        print(f"Total messages: {len(self.message_history)}")
        print(f"\nMessages per agent:")
        for agent_id, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True):
            color = self._get_agent_color(agent_id)
            agent_name = agent_id.replace("_", " ").title()
            print(f"  {color}{agent_name}{Style.RESET_ALL}: {count}")
    
    def save_chat_log(self, output_path: Path):
        """Save chat history to a file"""
        import json
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.message_history, f, indent=2, ensure_ascii=False)
        
        print(f"\n{self.ICONS['file']} Chat log saved to: {Fore.LIGHTBLUE_EX}{output_path}{Style.RESET_ALL}")


class ProgressTracker:
    """Track and display workflow progress with visual indicators"""
    
    def __init__(self, total_steps: int = 6):
        self.total_steps = total_steps
        self.current_step = 0
        self.step_names = []
        self.completed_unique_steps = set()  # Track unique completed steps
        
        # Define the expected workflow steps in order
        self.workflow_steps = [
            "business_analyst",
            "architecture_design", 
            "implementation",
            "qa_testing",
            "infrastructure",
            "documentation"
        ]
    
    def update(self, step_name: str):
        """Update progress with new step"""
        # Map node names to workflow steps
        step_mapping = {
            "business_analyst": "business_analyst",
            "architecture_design": "architecture_design",
            "implementation": "implementation",
            "qa_testing": "qa_testing",
            "infrastructure": "infrastructure",
            "documentation": "documentation"
        }
        
        # Get the workflow step name
        workflow_step = step_mapping.get(step_name, step_name)
        
        # Only increment if this is a new unique step
        if workflow_step not in self.completed_unique_steps:
            self.completed_unique_steps.add(workflow_step)
            self.current_step = len(self.completed_unique_steps)
            self.step_names.append(workflow_step)
            self._display_progress()
    
    def update_with_count(self, completed_steps_list: list):
        """Update progress based on completed steps list from state"""
        # Count unique completed steps
        unique_steps = set(completed_steps_list)
        self.current_step = len(unique_steps)
        self.completed_unique_steps = unique_steps
        
        if completed_steps_list:
            latest_step = completed_steps_list[-1]
            if latest_step not in self.step_names:
                self.step_names.append(latest_step)
        
        self._display_progress()
    
    def _display_progress(self):
        """Display progress bar and current step"""
        percentage = int((self.current_step / self.total_steps) * 100)
        bar_length = 40
        filled = int((self.current_step / self.total_steps) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        step_name = self.step_names[-1] if self.step_names else "Starting"
        
        print(f"\n{Fore.CYAN}Progress:{Style.RESET_ALL} {bar} {percentage}%")
        print(f"{Fore.CYAN}Current:{Style.RESET_ALL} {step_name}")
        print(f"{Fore.CYAN}Steps completed:{Style.RESET_ALL} {self.current_step}/{self.total_steps}")


def demo_chat_display():
    """Demonstrate the chat display capabilities"""
    chat = AgentChatDisplay()
    
    chat.print_header("Multi-Agent System - Interactive Demo")
    
    chat.system_message("Starting workflow...", "start")
    
    chat.agent_message(
        "business_analyst",
        "Analyzing requirements for the e-commerce platform...\nIdentifying key user stories and acceptance criteria.",
        message_type="thinking"
    )
    
    chat.agent_action("business_analyst", "is creating user stories", "Writing to: requirements.md")
    
    chat.agent_completed(
        "business_analyst",
        "Requirements analysis complete. Identified 5 user stories and 12 acceptance criteria.",
        files_created=["docs/requirements.md", "docs/user_stories.md"]
    )
    
    chat.inter_agent_communication(
        "business_analyst",
        "developer",
        "Passing requirements and user stories for architecture design",
        communication_type="handoff"
    )
    
    chat.agent_message(
        "developer",
        "Designing microservices architecture...\nPlanning: API Gateway, Product Service, Cart Service, Payment Service",
        message_type="thinking",
        to_agent="business_analyst"
    )
    
    chat.workflow_status(
        "workflow_20260113_120000",
        "running",
        "architecture_design",
        ["business_analyst", "architecture_design"]
    )
    
    chat.agent_completed(
        "developer",
        "Architecture design complete. Defined 4 microservices with REST APIs.",
        files_created=["architecture/system_design.md", "architecture/api_specs.yaml"]
    )
    
    chat.conversation_summary()


if __name__ == "__main__":
    demo_chat_display()
