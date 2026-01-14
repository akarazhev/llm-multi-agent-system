import asyncio
import logging
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from collections import defaultdict
from ..agents.base_agent import Task, AgentStatus

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.completed_tasks: Set[str] = set()
        self.failed_tasks: Set[str] = set()
        self.task_dependencies: Dict[str, List[str]] = defaultdict(list)
    
    def add_task(self, task: Task) -> None:
        self.tasks[task.task_id] = task
        
        if task.dependencies:
            self.task_dependencies[task.task_id] = task.dependencies
        
        logger.info(f"Added task {task.task_id} with priority {task.priority}")
    
    async def enqueue_task(self, task: Task) -> None:
        if not self._check_dependencies_met(task.task_id):
            logger.warning(f"Task {task.task_id} dependencies not met, waiting...")
            return
        
        await self.task_queue.put((-task.priority, task.task_id, task))
        logger.info(f"Enqueued task {task.task_id}")
    
    async def get_next_task(self) -> Optional[Task]:
        if self.task_queue.empty():
            return None
        
        _, task_id, task = await self.task_queue.get()
        return task
    
    def _check_dependencies_met(self, task_id: str) -> bool:
        dependencies = self.task_dependencies.get(task_id, [])
        
        for dep_id in dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        return True
    
    def mark_completed(self, task_id: str) -> None:
        self.completed_tasks.add(task_id)
        logger.info(f"Task {task_id} marked as completed")
        
        self._check_dependent_tasks(task_id)
    
    def mark_failed(self, task_id: str) -> None:
        self.failed_tasks.add(task_id)
        logger.error(f"Task {task_id} marked as failed")
    
    def _check_dependent_tasks(self, completed_task_id: str) -> None:
        for task_id, dependencies in self.task_dependencies.items():
            if completed_task_id in dependencies and task_id not in self.completed_tasks:
                if self._check_dependencies_met(task_id):
                    task = self.tasks.get(task_id)
                    if task:
                        asyncio.create_task(self.enqueue_task(task))
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        status = "pending"
        if task_id in self.completed_tasks:
            status = "completed"
        elif task_id in self.failed_tasks:
            status = "failed"
        
        return {
            "task_id": task.task_id,
            "description": task.description,
            "status": status,
            "priority": task.priority,
            "dependencies": task.dependencies,
            "created_at": task.created_at.isoformat(),
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
    
    def get_all_tasks_status(self) -> Dict[str, Any]:
        return {
            "total_tasks": len(self.tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
            "pending": len(self.tasks) - len(self.completed_tasks) - len(self.failed_tasks),
            "tasks": {
                task_id: self.get_task_status(task_id)
                for task_id in self.tasks.keys()
            }
        }
    
    def create_task_graph(self) -> Dict[str, Any]:
        graph = {
            "nodes": [],
            "edges": []
        }
        
        for task_id, task in self.tasks.items():
            status = "pending"
            if task_id in self.completed_tasks:
                status = "completed"
            elif task_id in self.failed_tasks:
                status = "failed"
            
            graph["nodes"].append({
                "id": task_id,
                "description": task.description,
                "status": status,
                "priority": task.priority
            })
            
            for dep_id in task.dependencies:
                graph["edges"].append({
                    "from": dep_id,
                    "to": task_id
                })
        
        return graph
