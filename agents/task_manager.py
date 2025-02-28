import logging
import re
from dataclasses import dataclass, field
from typing import List
from agents import scanner

@dataclass
class Task:
    name: str
    command: str
    parameters: dict
    retries: int = 0
    status: str = "Pending"
    output: str = ""

class TaskManager:
    def __init__(self, scope: str):
        self.scope = scope
        self.tasks: List[Task] = []
        self.logger = logging.getLogger("TaskManager")
    
    def parse_instruction(self, instruction: str):
        """
        Naively break down the high-level instruction into a list of tasks.
        You can later replace this with a LangGraph or LangChain parsing module.
        """
        # If instruction mentions nmap, add an nmap scan task.
        if "nmap" in instruction.lower():
            target = self.extract_target(instruction)
            task = Task(
                name="Nmap Scan",
                command="nmap",
                parameters={"target": target}
            )
            self.tasks.append(task)
        
        # If gobuster is mentioned, add a gobuster task.
        if "gobuster" in instruction.lower():
            target = self.extract_target(instruction)
            task = Task(
                name="Gobuster Scan",
                command="gobuster",
                parameters={"target": target}
            )
            self.tasks.append(task)
        
        # If ffuf is mentioned, add an ffuf task.
        if "ffuf" in instruction.lower():
            target = self.extract_target(instruction)
            task = Task(
                name="FFUF Scan",
                command="ffuf",
                parameters={"target": target}
            )
            self.tasks.append(task)
        
        # If sqlmap is mentioned, add an sqlmap task.
        if "sqlmap" in instruction.lower():
            target = self.extract_target(instruction)
            task = Task(
                name="SQLMap Test",
                command="sqlmap",
                parameters={"target": target}
            )
            self.tasks.append(task)
        
        # If zenmap is mentioned, add a visualization task.
        if "zenmap" in instruction.lower():
            task = Task(
                name="Visualization with Zenmap",
                command="zenmap",
                parameters={}
            )
            self.tasks.append(task)
    
    def extract_target(self, instruction: str) -> str:
        """
        Naively extract a domain or IP address from the instruction.
        This is a simple regex and can be extended for better accuracy.
        """
        pattern = r'((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
        match = re.search(pattern, instruction)
        if match:
            return match.group(1)
        # Fallback to the user-defined scope if extraction fails.
        return self.scope
    
    def enforce_scope(self, target: str) -> bool:
        """
        Ensure the target is within the allowed scope.
        For now, we check if the scope string is contained in the target.
        """
        if self.scope in target:
            return True
        return False
    
    def execute_tasks(self) -> List[str]:
        reports = []
        for task in self.tasks:
            self.logger.info(f"Executing task: {task.name}")
            target = task.parameters.get("target", "")
            if target and not self.enforce_scope(target):
                task.status = "Blocked"
                task.output = "Target outside allowed scope."
                reports.append(f"{task.name}: {task.status} - {task.output}")
                continue
            
            # Execute the scan based on the command type
            if task.command == "nmap":
                task.output = scanner.run_nmap(target)
            elif task.command == "gobuster":
                task.output = scanner.run_gobuster(target)
            elif task.command == "ffuf":
                task.output = scanner.run_ffuf(target)
            elif task.command == "sqlmap":
                task.output = scanner.run_sqlmap(target)
            elif task.command == "zenmap":
                task.output = "Visualization completed using Zenmap."
            else:
                task.output = "Unknown command."
            
            task.status = "Completed"
            reports.append(f"{task.name}: {task.status} - {task.output}")
        return reports
