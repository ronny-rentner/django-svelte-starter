#!/usr/bin/env python3

import os
import sys
from pathlib import Path

def find_venv(venv_dir):
    """Find or create a virtual environment."""
    venv_path = Path(venv_dir)
    if not venv_path.exists():
        raise Exception('Could not find venv directory')
    return venv_path

def run_in_venv(venv_path, main_script, *args):
    """Run the main script inside the virtual environment."""
    venv_python = venv_path / "bin" / "python"
    if not venv_python.exists():
        print(f"Python executable not found in virtual environment: {venv_python}")
        sys.exit(1)

    argv = [str(venv_python), str(main_script)] + list(args)
    os.execvp(str(venv_python), argv)

if __name__ == "__main__":
    script_dir = Path(__file__).parent.resolve()
    venv_dir = script_dir / "backend" / "venv"
    main_script = script_dir / "cli" / "cli.py"

    if not main_script.exists():
        print(f"Error: Main script not found at {main_script}")
        sys.exit(1)

    #main_script = "empty.py"
    venv_path = find_venv(venv_dir)

    # Run the main script inside the virtual environment
    run_in_venv(venv_path, main_script, *sys.argv[1:])

