#!/usr/bin/env python3
"""Install the non-inference Yawdie observation LaunchAgent."""
import argparse
import os
import plistlib
import shutil
import subprocess
from pathlib import Path

LABEL = 'com.major.hamal.yawdie.observer'
HOME = Path.home()
PLIST = HOME / 'Library/LaunchAgents' / f'{LABEL}.plist'
STATE = HOME / '.local/share/hamal-yawdie'
OPERATIONS = STATE / 'operations'
LOGS = HOME / 'Library/Logs/HAMAL/Yawdie'
RUNTIME = HOME / 'Library/Application Support/HAMAL/Yawdie/observer'
PYTHON = Path('/usr/bin/python3')
SOURCE = Path(__file__).resolve().parent


def evidence_paths(name):
    return (OPERATIONS / f'OVERNIGHT_OBSERVATION_{name}.jsonl',
            OPERATIONS / f'OVERNIGHT_OBSERVATION_{name}_FINAL.md')


def install(start, end, name, interval):
    evidence, summary = evidence_paths(name)
    for folder in (PLIST.parent, OPERATIONS, LOGS, RUNTIME):
        folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    shutil.copy2(SOURCE / 'observer.py', RUNTIME / 'observer.py')
    os.chmod(RUNTIME / 'observer.py', 0o700)
    config = {
        'Label': LABEL,
        'ProgramArguments': [str(PYTHON), str(RUNTIME / 'observer.py'),
                             '--database', str(STATE / 'state.sqlite'),
                             '--logs', str(LOGS), '--evidence', str(evidence),
                             '--summary', str(summary), '--start', start, '--end', end,
                             '--interval', str(interval)],
        'RunAtLoad': True,
        'StartInterval': interval,
        'ProcessType': 'Background',
        'StandardOutPath': str(LOGS / 'observer.stdout.log'),
        'StandardErrorPath': str(LOGS / 'observer.stderr.log'),
        'EnvironmentVariables': {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin'},
    }
    temporary = PLIST.with_suffix('.plist.tmp')
    with temporary.open('wb') as handle:
        plistlib.dump(config, handle, sort_keys=True)
    os.chmod(temporary, 0o600)
    os.replace(temporary, PLIST)
    domain = f'gui/{os.getuid()}'
    subprocess.run(['launchctl', 'bootout', domain, str(PLIST)], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['launchctl', 'bootstrap', domain, str(PLIST)], check=True)
    print(summary)


def status():
    return subprocess.run(['launchctl', 'print', f'gui/{os.getuid()}/{LABEL}']).returncode


def uninstall():
    subprocess.run(['launchctl', 'bootout', f'gui/{os.getuid()}', str(PLIST)], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    PLIST.unlink(missing_ok=True)
    if RUNTIME.exists():
        shutil.rmtree(RUNTIME)
    print(f'Observation evidence retained at {OPERATIONS}')


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('install')
    create.add_argument('--start', required=True)
    create.add_argument('--end', required=True)
    create.add_argument('--name', required=True)
    create.add_argument('--interval', type=int, default=900)
    sub.add_parser('status')
    sub.add_parser('uninstall')
    args = parser.parse_args()
    if args.command == 'install':
        return install(args.start, args.end, args.name, args.interval)
    if args.command == 'status':
        return status()
    return uninstall()


if __name__ == '__main__':
    raise SystemExit(main() or 0)
