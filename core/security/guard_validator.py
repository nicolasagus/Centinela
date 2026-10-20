import json
import os
import sys
from typing import List, Tuple

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "zero-trust.config.json")

class ZeroTrustEnforcer:
    def __init__(self, config_path: str = CONFIG_PATH):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuración Zero-Trust ausente en: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            self.policy = json.load(f).get("policy", {})

    def evaluate_command(self, cmd_tokens: List[str]) -> Tuple[bool, str]:
        if not cmd_tokens:
            return False, "Comando vacío denegado por defecto."

        binary = cmd_tokens[0].lower()
        args = cmd_tokens[1:]
        full_command_str = " ".join(cmd_tokens)

        # 1. Comprobar binario en whitelist
        allowed_cmds = self.policy.get("allowed_commands", [])
        rule = next((c for c in allowed_cmds if c.get("binary") == binary), None)

        if not rule:
            return False, f"ACCESO DENEGADO: El binario '{binary}' no pertenece a la whitelist."

        # 2. Validaciones específicas para Git
        if binary == "git":
            blocked_flags = rule.get("blocked_flags", [])
            for flag in blocked_flags:
                if flag in full_command_str:
                    return False, f"BLOQUEO ZERO-TRUST: Flag destructiva detectada '{flag}'."
            allowed_subs = rule.get("allowed_subcommands", [])
            if args and args[0] not in allowed_subs:
                return False, f"ACCESO DENEGADO: Subcomando de git '{args[0]}' no permitido."

        # 3. Validaciones específicas para Docker
        if binary == "docker":
            enforce_flags = rule.get("enforce_flags", [])
            for req_flag in enforce_flags:
                if req_flag not in full_command_str:
                    return False, f"SEGURIDAD INSUFICIENTE: Falta flag mandatoria en Docker: '{req_flag}'."

        return True, "COMANDO AUTORIZADO"

if __name__ == "__main__":
    enforcer = ZeroTrustEnforcer()
    
    # Pruebas de sanidad automáticas
    test_cases = [
        ["git", "status"],
        ["git", "push", "--force"],
        ["docker", "run", "--rm", "--network=none", "--memory=1g", "--cpus=2", "alpine:latest"],
        ["docker", "run", "ubuntu:latest"],
        ["rmdir", "/s", "/q", "C:\\"]
    ]

    print("[ZeroTrustGuard] Ejecutando suite de verificación interna...")
    for cmd in test_cases:
        allowed, msg = enforcer.evaluate_command(cmd)
        verdict = "PASS" if allowed else "BLOCK"
        print(f"[{verdict}] {' '.join(cmd)} -> {msg}")