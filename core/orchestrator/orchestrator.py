import json
import os
import sys
import time
from typing import Dict, Any

# 1. Resolucion rigida de paths: inyecta core/ y la raiz del proyecto en sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(CORE_DIR)

for path in [CORE_DIR, ROOT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# 2. Importaciones con fallback para ejecucion desde cualquier contexto
try:
    from security.guard_validator import ZeroTrustEnforcer
    from gateway.approval_gateway import ApprovalGateway
    from telemetry.telemetry_engine import TelemetryEngine
except ModuleNotFoundError:
    from core.security.guard_validator import ZeroTrustEnforcer
    from core.gateway.approval_gateway import ApprovalGateway
    from core.telemetry.telemetry_engine import TelemetryEngine


class MasterOrchestrator:
    def __init__(self, gateway_mode: str = "MOCK_GATE"):
        self.security_guard = ZeroTrustEnforcer()
        self.human_gateway = ApprovalGateway(mode=gateway_mode)
        self.telemetry = TelemetryEngine()
        self.task_history = []

    def dispatch(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_id = task.get("task_id", "unknown")
        cmd = task.get("command", [])
        risk_level = task.get("risk_level", "LOW")
        start_time = time.time()

        # Gate 1: Validacion perimetral Zero-Trust
        allowed, reason = self.security_guard.evaluate_command(cmd)
        if not allowed:
            task["status"] = "REJECTED_SECURITY"
            task["error"] = reason
            self.task_history.append(task)
            self.telemetry.record_event("ZERO_TRUST_BLOCK", {
                "task_id": task_id,
                "command": cmd,
                "reason": reason
            })
            return task

        # Gate 2: Human-in-the-Loop Gateway
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
                self.telemetry.record_event("HUMAN_GATE_VETO", {
                    "task_id": task_id,
                    "command": cmd
                })
                return task

        # Gate 3: Despacho a Worker
        duration_ms = round((time.time() - start_time) * 1000, 2)
        task["status"] = "COMPLETED"
        task["output"] = f"Worker '{task.get('assigned_worker')}' ejecuto exitosamente: {' '.join(cmd)}"
        self.task_history.append(task)
        self.telemetry.record_event("TASK_COMPLETED", {
            "task_id": task_id,
            "assigned_worker": task.get("assigned_worker"),
            "duration_ms": duration_ms
        })
        return task


if __name__ == "__main__":
    orchestrator = MasterOrchestrator(gateway_mode="MOCK_GATE")

    tasks = [
        {
            "task_id": "TASK-001",
            "assigned_worker": "docker-runner",
            "command": ["docker", "run", "--rm", "--network=none", "--memory=1g", "--cpus=2", "alpine:latest"],
            "risk_level": "HIGH",
            "requires_approval": True,
            "mock_decision": True
        },
        {
            "task_id": "TASK-002",
            "assigned_worker": "docker-runner",
            "command": ["docker", "run", "--rm", "--network=none", "--memory=1g", "--cpus=2", "alpine:latest"],
            "risk_level": "HIGH",
            "requires_approval": True,
            "mock_decision": False
        },
        {
            "task_id": "TASK-003",
            "assigned_worker": "docker-runner",
            "command": ["git", "push", "--force"],
            "risk_level": "HIGH"
        }
    ]

    print("[MasterOrchestrator] Despachando con telemetria en tiempo real:")
    for t in tasks:
        res = orchestrator.dispatch(t)
        detail = res.get("output") or res.get("error")
        print(f"[{res['status']}] {res['task_id']} -> {detail}")

    print("\n[Telemetry Summary]:")
    print(json.dumps(orchestrator.telemetry.get_summary(), indent=2))