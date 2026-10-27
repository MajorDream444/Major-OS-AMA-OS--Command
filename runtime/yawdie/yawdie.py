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
import vault
import repository
import production


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
    vault_command = sub.add_parser('vault', help='operate the approved Major OS bridge')
    vault_command.add_argument('--root', type=Path, required=True)
    vault_sub = vault_command.add_subparsers(dest='vault_action', required=True)
    vault_sub.add_parser('init')
    vault_submit = vault_sub.add_parser('submit')
    vault_submit.add_argument('--source', required=True)
    vault_submit.add_argument('--rerun', action='store_true')
    vault_submit.add_argument('--day', default=datetime.now(ZoneInfo('Asia/Makassar')).date().isoformat())
    vault_scan = vault_sub.add_parser('scan')
    vault_scan.add_argument('--day', default=datetime.now(ZoneInfo('Asia/Makassar')).date().isoformat())
    vault_export = vault_sub.add_parser('export')
    vault_export.add_argument('--job-id', required=True)
    repo = sub.add_parser('repository', help='snapshot explicitly approved local repositories')
    repo.add_argument('--manifest', type=Path, required=True)
    repo.add_argument('--name', action='append', required=True)
    repo.add_argument('--vault-root', type=Path)
    repo.add_argument('--output-name')
    prod = sub.add_parser('production', help='operate the bounded recording-to-review queue')
    prod_sub = prod.add_subparsers(dest='production_action', required=True)
    prod_ack = prod_sub.add_parser('acknowledge')
    prod_ack.add_argument('--implementation-commit', required=True)
    prod_ack.add_argument('--runtime-identity', required=True)
    prod_sub.add_parser('acknowledgment')
    prod_submit = prod_sub.add_parser('submit')
    prod_submit.add_argument('--config', type=Path, required=True)
    prod_submit.add_argument('--manifest', type=Path, required=True)
    prod_status = prod_sub.add_parser('status')
    prod_status.add_argument('--job-id')
    args = parser.parse_args()

    root = Path(args.state).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    if args.command == 'service':
        return subprocess.run([sys.executable, str(Path(__file__).with_name('service.py')), args.action]).returncode
    if args.command == 'vault' and args.vault_action == 'init':
        print(json.dumps({'created': vault.initialize_layout(args.root)}, indent=2))
        return 0
    if args.command == 'repository':
        snapshots = repository.snapshot_named(args.manifest, args.name)
        content = repository.markdown(snapshots)
        if args.vault_root or args.output_name:
            if not args.vault_root or not args.output_name:
                parser.error('--vault-root and --output-name must be supplied together')
            output = repository.export_context(args.vault_root, args.output_name,
                                               repository.context_markdown(snapshots))
            print(json.dumps({'repositories': args.name, 'context': output,
                              'snapshots': {name: {'commit': item['commit'], 'dirty': item['dirty'],
                                                   'snapshot_sha256': item['snapshot_sha256']}
                                            for name, item in snapshots.items()}}, indent=2))
        else:
            print(content)
        return 0
    db = worker.connect(root / 'state.sqlite')
    try:
        if args.command == 'production':
            if args.production_action == 'acknowledge':
                result = production.acknowledge(db, args.implementation_commit, args.runtime_identity)
            elif args.production_action == 'acknowledgment':
                result = production.acknowledgment(db)
            elif args.production_action == 'submit':
                result = production.submit(db, args.config, args.manifest)
            else:
                result = production.report(db, args.job_id)
            print(json.dumps(result, indent=2))
        elif args.command == 'brief':
            if args.task not in worker.TASK_FIELDS:
                print(json.dumps({'status': 'blocked', 'reason': 'adapter unavailable', 'task': args.task}))
                return 2
            source = args.source.expanduser().resolve()
            body = source.read_text()
            job_id = worker.enqueue(db, 'maim', body, args.reference or str(source), args.day,
                                    task=args.task, rerun=args.rerun)
            print(json.dumps({'status': 'queued', 'job_id': job_id, 'workflow': args.task,
                              'intentional_rerun': args.rerun}))
        elif args.command == 'vault':
            if args.vault_action == 'submit':
                result = vault.submit(db, args.root, args.source, args.day, args.rerun)
            elif args.vault_action == 'scan':
                result = vault.scan(db, args.root, args.day)
            else:
                result = vault.export_report(db, args.root, args.job_id)
            print(json.dumps(result, indent=2))
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
