import json
import os
import sys
from typing import Dict, Any

# Inyecta core/ directamente al PATH de importacion
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.dirname(CURRENT_DIR)
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

from security.guard_validator import ZeroTrustEnforcer

class MasterOrchestrator:
    def __init__(self):
        self.security_guard = ZeroTrustEnforcer()
        self.task_history = []

    def dispatch(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_id = task.get("task_id", "unknown")
        cmd = task.get("command", [])

        # 1. Gate de validacion Zero-Trust
        allowed, reason = self.security_guard.evaluate_command(cmd)
        if not allowed:
            task["status"] = "REJECTED_SECURITY"
            task["error"] = reason
            self.task_history.append(task)
            return task

        # 2. Despacho a Worker
        task["status"] = "COMPLETED"
        task["output"] = f"Worker '{task.get('assigned_worker')}' ejecuto exitosamente: {' '.join(cmd)}"
        self.task_history.append(task)
        return task

if __name__ == "__main__":
    orchestrator = MasterOrchestrator()

    # Tarea valida para worker de docker
    valid_task = {
        "task_id": "TASK-001",
        "assigned_worker": "docker-runner",
        "command": ["docker", "run", "--rm", "--network=none", "--memory=1g", "--cpus=2", "alpine:latest"],
        "sandbox_isolated": True,
        "status": "PENDING"
    }

    # Tarea maliciosa o invalida
    invalid_task = {
        "task_id": "TASK-002",
        "assigned_worker": "docker-runner",
        "command": ["git", "push", "--force"],
        "sandbox_isolated": False,
        "status": "PENDING"
    }

    res_1 = orchestrator.dispatch(valid_task)
    print(f"[{res_1['status']}] {res_1['task_id']} -> {res_1.get('output', res_1.get('error'))}")

    res_2 = orchestrator.dispatch(invalid_task)
    print(f"[{res_2['status']}] {res_2['task_id']} -> {res_2.get('output', res_2.get('error'))}")