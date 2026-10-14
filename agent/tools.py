import subprocess
from datetime import datetime, timezone


def get_time() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_diagnostic(cmd: str, expression: str = "0") -> str:
    """Unsafe scan fixture; never expose via HTTP or pass untrusted input."""
    # DEMO-ONLY: intentional finding - user-supplied shell command (B602).
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # DEMO-ONLY: intentional finding - evaluation of user input (B307).
    evaluated = eval(expression)
    return f"{result.stdout.strip()}\n{evaluated}"
