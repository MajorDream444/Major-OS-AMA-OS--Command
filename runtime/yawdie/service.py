#!/usr/bin/env python3
"""Install and control Yawdie's per-user macOS LaunchAgent."""
import argparse
import os
import plistlib
import shutil
import subprocess
import time
from pathlib import Path

LABEL = 'com.major.hamal.yawdie'
HOME = Path.home()
PLIST = HOME / 'Library/LaunchAgents' / f'{LABEL}.plist'
STATE = HOME / '.local/share/hamal-yawdie'
INBOX = STATE / 'inbox'
LOGS = HOME / 'Library/Logs/HAMAL/Yawdie'
BIN = HOME / '.local/bin/yawdie'
MODEL = 'llama3.2:latest'
SOURCE = Path(__file__).resolve().parent
RUNTIME = HOME / 'Library/Application Support/HAMAL/Yawdie/runtime'
PYTHON = Path('/usr/bin/python3')


def program_arguments(vault_root=None):
    args = [str(PYTHON), str(RUNTIME / 'worker.py'), '--state', str(STATE),
            'loop', '--model', MODEL, '--inbox', str(INBOX)]
    if vault_root:
        args.extend(['--vault-root', str(Path(vault_root).expanduser().resolve(strict=True))])
    return args


def run(*args, check=True):
    return subprocess.run(args, check=check)


def install():
    vault_root = os.environ.get('YAWDIE_VAULT_ROOT')
    if vault_root:
        from path_policy import PathPolicy
        PathPolicy(vault_root, ('Yawdie/Context', 'Yawdie/Briefs/Inbox',
                                'Yawdie/Reports', 'Yawdie/Templates'))
    stop()
    for folder in (PLIST.parent, STATE, INBOX, LOGS, BIN.parent, RUNTIME):
        folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name in ('worker.py', 'yawdie.py', 'service.py', 'vault.py', 'path_policy.py',
                 'repository.py', 'production.py'):
        shutil.copy2(SOURCE / name, RUNTIME / name)
        os.chmod(RUNTIME / name, 0o700)
    launcher = '#!/bin/sh\nexec /usr/bin/python3 ' + repr(str(RUNTIME / 'yawdie.py')) + ' "$@"\n'
    BIN.write_text(launcher)
    os.chmod(BIN, 0o700)
    config = {
        'Label': LABEL,
        'ProgramArguments': program_arguments(vault_root),
        'RunAtLoad': True,
        'KeepAlive': {'SuccessfulExit': False},
        'ThrottleInterval': 30,
        'ProcessType': 'Background',
        'WorkingDirectory': str(RUNTIME),
        'StandardOutPath': str(LOGS / 'stdout.log'),
        'StandardErrorPath': str(LOGS / 'stderr.log'),
        'EnvironmentVariables': {'PATH': '/opt/homebrew/bin:/usr/bin:/bin'},
    }
    with PLIST.open('wb') as f:
        plistlib.dump(config, f, sort_keys=True)
    os.chmod(PLIST, 0o600)
    start()


def model_is_installed():
    result = subprocess.run(['/opt/homebrew/bin/ollama', 'list'], capture_output=True, text=True)
    if result.returncode != 0:
        return False
    return any(line.split() and line.split()[0] == MODEL for line in result.stdout.splitlines()[1:])


def loaded_state():
    result = subprocess.run(['launchctl', 'print', f'gui/{os.getuid()}/{LABEL}'],
                            capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return 'running' if 'state = running' in result.stdout else 'loaded'


def start():
    os.umask(0o077)
    for folder in (STATE, INBOX, LOGS, RUNTIME):
        if folder.exists():
            os.chmod(folder, 0o700)
    for log in (LOGS / 'stdout.log', LOGS / 'stderr.log'):
        if log.exists():
            os.chmod(log, 0o600)
    domain = f'gui/{os.getuid()}'
    state = loaded_state()
    if state == 'running':
        return
    if not model_is_installed():
        raise SystemExit(f'Required local model is not installed: {MODEL}')
    if state == 'loaded':
        run('launchctl', 'kickstart', f'{domain}/{LABEL}')
        return
    last = None
    for _ in range(5):
        last = subprocess.run(['launchctl', 'bootstrap', domain, str(PLIST)],
                              capture_output=True, text=True)
        if last.returncode == 0:
            return
        time.sleep(0.5)
    raise SystemExit((last.stderr or 'launchctl bootstrap failed').strip())


def stop():
    subprocess.run(['launchctl', 'bootout', f'gui/{os.getuid()}', str(PLIST)],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def status():
    return run('launchctl', 'print', f'gui/{os.getuid()}/{LABEL}', check=False).returncode


def uninstall():
    stop()
    if PLIST.exists():
        PLIST.unlink()
    if BIN.exists() and str(RUNTIME / 'yawdie.py') in BIN.read_text():
        BIN.unlink()
    if RUNTIME.exists():
        shutil.rmtree(RUNTIME)
    print(f'Private state retained at {STATE}; remove it manually only if its job history is no longer needed.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=('install', 'start', 'stop', 'status', 'uninstall'))
    a = p.parse_args()
    return {'install': install, 'start': start, 'stop': stop,
            'status': status, 'uninstall': uninstall}[a.command]() or 0


if __name__ == '__main__':
    raise SystemExit(main())
