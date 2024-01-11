# src/tools/pnpm.py

import subprocess


def execute_pnpm_command(command: str) -> str:
    try:
        result = subprocess.run(["pnpm", *command.split()], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to execute pnpm command: {e}") from e
