# src/tools/apt.py

import subprocess


def execute_apt_command(command: str) -> str:
    try:
        result = subprocess.run(["pnpm.py", *command.split()], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to execute pnpm command: {e}") from e
