import logging
from agents.task_manager import TaskManager

class CyberSecurityAgent:
    def __init__(self, scope: str):
        self.scope = scope
        self.task_manager = TaskManager(scope)
        self.logger = logging.getLogger("CyberSecurityAgent")
        logging.basicConfig(level=logging.INFO)
    
    def run(self, instruction: str) -> str:
        # Parse instruction into individual tasks
        self.logger.info("Parsing instruction into tasks.")
        self.task_manager.parse_instruction(instruction)
        
        # Execute tasks sequentially, handling failures and scope enforcement
        self.logger.info("Executing tasks.")
        task_reports = self.task_manager.execute_tasks()
        
        # Generate a final report summarizing each task's output
        self.logger.info("Generating final report.")
        final_report = self.generate_report(task_reports)
        return final_report
    
    def generate_report(self, task_reports):
        report = "Cybersecurity Audit Report\n"
        report += "=============================\n\n"
        for line in task_reports:
            report += f"{line}\n"
        return report
