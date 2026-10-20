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
from gateway.approval_gateway import ApprovalGateway

class MasterOrchestrator:
    def __init__(self, gateway_mode: str = "MOCK_GATE"):
        self.security_guard = ZeroTrustEnforcer()
        self.human_gateway = ApprovalGateway(mode=gateway_mode)
        self.task_history = []

    def dispatch(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_id = task.get("task_id", "unknown")
        cmd = task.get("command", [])
        risk_level = task.get("risk_level", "LOW")

        # 1. Gate de validacion Zero-Trust
        allowed, reason = self.security_guard.evaluate_command(cmd)
        if not allowed:
            task["status"] = "REJECTED_SECURITY"
            task["error"] = reason
            self.task_history.append(task)
            return task

        # 2. Gate Human-in-the-Loop si el riesgo es HIGH o se exige explicitamente
        if task.get("requires_approval", False) or risk_level == "HIGH":
            task["status"] = "GATE_PENDING"
            mock_decision = task.get("mock_decision", True)
            approved = self.human_gateway.request_approval(
                task_id=task_id,
                action="DISPATCH_WORKER_COMMAND",
                details={"command": cmd, "risk_level": risk_level, "mock_decision": mock_decision}
            )
            if not approved:
                task["status"] = "REJECTED_BY_OPERATOR"
                task["error"] = "Rechazado por el operador humano en compuerta interactiva."
                self.task_history.append(task)
                return task

        # 3. Despacho a Worker
        task["status"] = "COMPLETED"
        task["output"] = f"Worker '{task.get('assigned_worker')}' ejecuto exitosamente: {' '.join(cmd)}"
        self.task_history.append(task)
        return task

if __name__ == "__main__":
    orchestrator = MasterOrchestrator(gateway_mode="MOCK_GATE")

    # Tarea 1: Valida con compuerta humana aprobada
    task_approved = {
        "task_id": "TASK-001",
        "assigned_worker": "docker-runner",
        "command": ["docker", "run", "--rm", "--network=none", "--memory=1g", "--cpus=2", "alpine:latest"],
        "risk_level": "HIGH",
        "requires_approval": True,
        "mock_decision": True
    }

    # Tarea 2: Valida en Zero-Trust pero rechazada por el operador humano
    task_vetoed = {
        "task_id": "TASK-002",
        "assigned_worker": "docker-runner",
        "command": ["docker", "run", "--rm", "--network=none", "--memory=1g", "--cpus=2", "alpine:latest"],
        "risk_level": "HIGH",
        "requires_approval": True,
        "mock_decision": False
    }

    # Tarea 3: Bloqueo directo en Zero-Trust (ni llega al operador)
    task_blocked = {
        "task_id": "TASK-003",
        "assigned_worker": "docker-runner",
        "command": ["git", "push", "--force"],
        "risk_level": "HIGH"
    }

    print("[MasterOrchestrator] Probando despacho coordinado:")
    for t in [task_approved, task_vetoed, task_blocked]:
        res = orchestrator.dispatch(t)
        detail = res.get("output") or res.get("error")
        print(f"[{res['status']}] {res['task_id']} -> {detail}")