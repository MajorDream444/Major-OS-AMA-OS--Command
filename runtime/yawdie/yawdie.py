#!/usr/bin/env python3
"""Operator CLI for Yawdie's bounded local source-to-draft runtime."""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import worker


DEFAULT_STATE = Path.home() / '.local/share/hamal-yawdie'


def main():
    parser = argparse.ArgumentParser(prog='yawdie')
    parser.add_argument('--state', default=os.environ.get('YAWDIE_STATE', str(DEFAULT_STATE)))
    sub = parser.add_subparsers(dest='command', required=True)
    brief = sub.add_parser('brief', help='submit a source for a daily brief draft')
    brief.add_argument('--source', type=Path, required=True)
    brief.add_argument('--reference')
    brief.add_argument('--task', default='source-to-draft')
    brief.add_argument('--rerun', action='store_true', help='intentionally create a new job for unchanged content')
    brief.add_argument('--day', default=datetime.now(ZoneInfo('Asia/Makassar')).date().isoformat())
    sub.add_parser('status', help='show queue and local service status')
    report = sub.add_parser('report', help='show job results and evidence')
    report.add_argument('--job-id')
    service = sub.add_parser('service', help='control the local LaunchAgent')
    service.add_argument('action', choices=('start', 'stop', 'uninstall'))
    args = parser.parse_args()

    root = Path(args.state).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    if args.command == 'service':
        return subprocess.run([sys.executable, str(Path(__file__).with_name('service.py')), args.action]).returncode
    db = worker.connect(root / 'state.sqlite')
    try:
        if args.command == 'brief':
            if args.task not in worker.TASK_FIELDS:
                print(json.dumps({'status': 'blocked', 'reason': 'adapter unavailable', 'task': args.task}))
                return 2
            source = args.source.expanduser().resolve()
            body = source.read_text()
            job_id = worker.enqueue(db, 'maim', body, args.reference or str(source), args.day,
                                    task=args.task, rerun=args.rerun)
            print(json.dumps({'status': 'queued', 'job_id': job_id, 'workflow': args.task,
                              'intentional_rerun': args.rerun}))
        elif args.command == 'status':
            data = worker.status(db)
            label = 'com.major.hamal.yawdie'
            proc = subprocess.run(['launchctl', 'print', f'gui/{os.getuid()}/{label}'],
                                  capture_output=True, text=True)
            data['service'] = 'running' if proc.returncode == 0 and 'state = running' in proc.stdout else 'stopped'
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps(worker.job_report(db, args.job_id), indent=2))
    finally:
        db.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
