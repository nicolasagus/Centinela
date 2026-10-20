import json
import os
import time
from typing import Dict, Any

class TelemetryEngine:
    def __init__(self, log_filename: str = "audit-telemetry.jsonl"):
        self.log_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", log_filename)
        )

    def record_event(self, event_type: str, payload: Dict[str, Any]):
        entry = {
            "timestamp": time.time(),
            "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event_type": event_type,
            "data": payload
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_summary(self) -> Dict[str, int]:
        if not os.path.exists(self.log_path):
            return {"total_events": 0}
        
        summary = {"total_events": 0, "security_blocks": 0, "operator_vetoes": 0, "completed": 0}
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                evt = json.loads(line)
                summary["total_events"] += 1
                ev_type = evt.get("event_type")
                if ev_type == "ZERO_TRUST_BLOCK":
                    summary["security_blocks"] += 1
                elif ev_type == "HUMAN_GATE_VETO":
                    summary["operator_vetoes"] += 1
                elif ev_type == "TASK_COMPLETED":
                    summary["completed"] += 1
        return summary

if __name__ == "__main__":
    telemetry = TelemetryEngine()
    print("[TelemetryEngine] Escribiendo eventos de calibración...")
    
    telemetry.record_event("TASK_COMPLETED", {"task_id": "TASK-001", "worker": "docker-runner", "duration_ms": 120})
    telemetry.record_event("HUMAN_GATE_VETO", {"task_id": "TASK-002", "reason": "Operator denied"})
    telemetry.record_event("ZERO_TRUST_BLOCK", {"task_id": "TASK-003", "flag": "--force"})

    stats = telemetry.get_summary()
    print(f"Resumen de telemetría generado: {json.dumps(stats, indent=2)}")
    print(f"Archivo registrado en: {telemetry.log_path}")