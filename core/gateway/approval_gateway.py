import json
import os
import sys
import time
from typing import Dict, Any, Optional

class ApprovalGateway:
    def __init__(self, mode: str = "CLI", auto_approve_safe: bool = False):
        self.mode = mode.upper()
        self.auto_approve_safe = auto_approve_safe
        self.audit_trail = []

    def request_approval(self, task_id: str, action: str, details: Dict[str, Any]) -> bool:
        prompt_payload = {
            "task_id": task_id,
            "action": action,
            "details": details,
            "timestamp": time.time(),
            "status": "PENDING"
        }

        # Auto-aprobacion para acciones categorizadas como seguras si la flag esta activa
        if self.auto_approve_safe and details.get("risk_level") == "LOW":
            prompt_payload["status"] = "APPROVED_AUTOMATIC"
            self.audit_trail.append(prompt_payload)
            return True

        if self.mode == "CLI":
            print("\n" + "=" * 60)
            print(f"[HUMAN-IN-THE-LOOP GATEWAY] Requiere Aprobación Humana")
            print(f"Tarea: {task_id}")
            print(f"Acción: {action}")
            print(f"Riesgo: {details.get('risk_level', 'MEDIUM')}")
            print(f"Detalles: {json.dumps(details, indent=2)}")
            print("=" * 60)
            
            # En entorno interactivo pide confirmacion; soporta mock para tests
            response = input("¿Aprobar ejecución? [s/N]: ").strip().lower()
            approved = response in ["s", "si", "y", "yes"]
            prompt_payload["status"] = "APPROVED" if approved else "REJECTED"
            self.audit_trail.append(prompt_payload)
            return approved

        elif self.mode == "MOCK_GATE":
            # Modo no bloqueante para suites de prueba automatizadas
            mock_verdict = details.get("mock_decision", True)
            prompt_payload["status"] = "APPROVED" if mock_verdict else "REJECTED"
            self.audit_trail.append(prompt_payload)
            return mock_verdict

        return False

if __name__ == "__main__":
    # Prueba rapida en modo simulado para verificar auditoria de transicion
    gateway = ApprovalGateway(mode="MOCK_GATE")

    print("[ApprovalGateway] Verificando flujo de compuertas...")
    approved = gateway.request_approval(
        task_id="TASK-DEPLOY-001",
        action="DOCKER_CONTAINER_START",
        details={"risk_level": "HIGH", "target": "alpine:latest", "mock_decision": True}
    )
    print(f"Decisión registrada: {'APROBADA' if approved else 'RECHAZADA'}")
    print(f"Registro en auditoría: {gateway.audit_trail[-1]['status']}")