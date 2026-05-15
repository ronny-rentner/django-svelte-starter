#!/usr/bin/env python3
import os, pty, subprocess, codecs, errno, signal, shlex, sys, time
from types import SimpleNamespace

def run_command(command, env=None):
    """
    Unix-only: run *command* through a PTY and stream output.
    Accepts EITHER a str *or* a list.  If str → shlex.split().
    """
    if isinstance(command, str):
        command = shlex.split(command)          # <-- key line

    env = env or os.environ.copy()

    master, slave = pty.openpty()
    proc = subprocess.Popen(
        command,
        stdin=slave, stdout=slave, stderr=slave,
        env=env, text=False
    )
    os.close(slave)

    # Forward Ctrl-C
    def fwd(sig, _):
        if proc.poll() is None:
            proc.send_signal(sig)
    signal.signal(signal.SIGINT, fwd)

    dec = codecs.getincrementaldecoder("utf-8")()
    try:
        while True:
            try:
                chunk = os.read(master, 1024)
            except OSError as e:
                if e.errno == errno.EIO:   # EOF
                    break
                raise
            if not chunk:
                break
            print(dec.decode(chunk), end="")
    finally:
        os.close(master)
        proc.wait()
    return SimpleNamespace(returncode=proc.returncode)

# ───── demo: launch one-liner that changes its proc title ─────
if __name__ == "__main__":
    pycode = (
        "import os,time,setproctitle;"
        "setproctitle.setproctitle('demo-child');"
        "print('child pid', os.getpid());"
        "time.sleep(30)"
    )
    cmd_str = f"{sys.executable} -c \"{pycode}\""   # <-- plain STRING
    print("parent pid", os.getpid())
    run_command(cmd_str)
