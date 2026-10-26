#!/usr/bin/env python3
"""Deterministic Yawdie health observer. It never invokes a model."""
import argparse
import fcntl
import json
import os
import re
import socket
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ZONE = ZoneInfo('Asia/Makassar')
LABEL = 'com.major.hamal.yawdie'


def launchd_snapshot():
    result = subprocess.run(
        ['launchctl', 'print', f'gui/{os.getuid()}/{LABEL}'],
        capture_output=True, text=True, timeout=10)
    text = result.stdout
    def value(pattern):
        match = re.search(pattern, text, re.M)
        return match.group(1).strip() if match else None
    return {
        'loaded': result.returncode == 0,
        'state': value(r'^\s*state = (.+)$'),
        'pid': value(r'^\s*pid = (\d+)$'),
        'runs': value(r'^\s*runs = (\d+)$'),
        'last_exit': value(r'^\s*last exit code = (.+)$'),
    }


def queue_snapshot(database):
    uri = 'file:' + quote(str(Path(database).resolve())) + '?mode=ro'
    connection = sqlite3.connect(uri, uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    try:
        counts = {row['status']: row['count'] for row in connection.execute(
            'SELECT status,count(*) count FROM jobs GROUP BY status')}
        jobs = []
        for row in connection.execute('SELECT id,status,attempts,task FROM jobs ORDER BY rowid'):
            attempts = [dict(item) for item in connection.execute(
                'SELECT attempt_number,status,failure_class FROM execution_attempts '
                'WHERE job_id=? ORDER BY started_at', (row['id'],))]
            jobs.append({**dict(row), 'attempt_history': attempts})
        return {'available': True, 'counts': counts, 'jobs': jobs}
    finally:
        connection.close()


def log_snapshot(log_directory):
    result = {}
    for name in ('stdout.log', 'stderr.log'):
        target = Path(log_directory) / name
        try:
            stat = target.stat()
            result[name] = {'bytes': stat.st_size, 'mtime': stat.st_mtime}
        except OSError:
            result[name] = {'unavailable': True}
    return result


def ollama_reachable():
    try:
        with socket.create_connection(('127.0.0.1', 11434), timeout=2):
            return True
    except OSError:
        return False


def snapshot(database, log_directory, now=None):
    now = now or datetime.now(ZONE)
    record = {
        'schema': 1,
        'observed_at': now.isoformat(),
        'yawdie': launchd_snapshot(),
        'ollama_loopback_reachable': ollama_reachable(),
        'logs': log_snapshot(log_directory),
    }
    try:
        record['queue'] = queue_snapshot(database)
    except (OSError, sqlite3.Error):
        record['queue'] = {'available': False}
    return record


def append_record(target, record):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with target.open('a', encoding='utf-8') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.write(json.dumps(record, sort_keys=True) + '\n')
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(target, 0o600)


def read_records(target):
    records = []
    try:
        lines = Path(target).read_text().splitlines()
    except OSError:
        return records
    for line in lines:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def sleep_events(start, end):
    try:
        result = subprocess.run(['/usr/bin/pmset', '-g', 'log'], capture_output=True,
                                text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return []
    events = []
    pattern = re.compile(
        r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4}).*'
        r'(Entering Sleep state|Wake from|DarkWake from)')
    for line in result.stdout.splitlines():
        match = pattern.search(line)
        if not match:
            continue
        try:
            at = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S %z')
        except ValueError:
            continue
        if start <= at <= end:
            events.append({'at': at.isoformat(), 'event': match.group(2)})
    return events


def gaps(records, start, end, interval_seconds):
    observed = sorted(datetime.fromisoformat(item['observed_at']) for item in records)
    points = [start, *observed, end]
    threshold = interval_seconds * 1.75
    return [
        {'from': left.isoformat(), 'to': right.isoformat(),
         'seconds': int((right - left).total_seconds())}
        for left, right in zip(points, points[1:])
        if (right - left).total_seconds() > threshold
    ]


def write_summary(target, records, start, end, interval_seconds):
    target = Path(target)
    if target.exists():
        return False
    gap_items = gaps(records, start, end, interval_seconds)
    sleeps = sleep_events(start, end)
    service_failures = [item['observed_at'] for item in records
                        if item.get('yawdie', {}).get('state') != 'running']
    ollama_failures = [item['observed_at'] for item in records
                       if not item.get('ollama_loopback_reachable')]
    queue_failures = [item['observed_at'] for item in records
                      if not item.get('queue', {}).get('available')]
    final_queue = records[-1].get('queue', {}) if records else {}
    final_jobs = final_queue.get('jobs', [])
    failed_jobs = [item for item in final_jobs if item['status'] in ('retry', 'blocked')]
    status = 'COMPLETE_WITH_GAPS_OR_FAILURES' if (
        gap_items or service_failures or ollama_failures or queue_failures or failed_jobs
    ) else 'COMPLETE'
    lines = [
        '# Yawdie local overnight observation', '',
        f'Status: {status}', '',
        '## Window', '',
        f'- Start: {start.isoformat()}',
        f'- End: {end.isoformat()}',
        f'- Snapshots: {len(records)}',
        f'- Intended interval: {interval_seconds} seconds',
        '- Observer: deterministic local process; no model calls', '',
        '## Health', '',
        f'- Yawdie service non-running snapshots: {len(service_failures)}',
        f'- Ollama loopback-unreachable snapshots: {len(ollama_failures)}',
        f'- Queue-unavailable snapshots: {len(queue_failures)}',
        f'- Final queue counts: `{json.dumps(final_queue.get("counts", {}), sort_keys=True)}`', '',
        '## Job outcomes', '',
    ]
    if final_jobs:
        for job in final_jobs:
            first = job['attempt_history'][0]['status'] if job['attempt_history'] else 'not_attempted'
            lines.append(
                f"- `{job['id']}`: first recorded attempt `{first}`; eventual `{job['status']}`; "
                f"attempts `{job['attempts']}`")
    else:
        lines.append('- No jobs were present in the final queue snapshot.')
    lines.extend(['', '## Observation gaps', ''])
    if gap_items:
        for gap in gap_items:
            lines.append(f"- {gap['from']} to {gap['to']} ({gap['seconds']} seconds)")
    else:
        lines.append('- No interval exceeded the configured gap threshold.')
    lines.extend(['', '## Sleep evidence', ''])
    if sleeps:
        for item in sleeps:
            lines.append(f"- {item['at']}: {item['event']}")
    else:
        lines.append('- No matching sleep/wake event was found. Sleep/wake recovery remains untested.')
    lines.extend([
        '', '## Interpretation', '',
        '- A timestamp gap is evidence that observation was absent; it is not by itself proof of sleep.',
        '- Idle service health is separate from interrupted-job recovery.',
        '- This observer does not prove Yawdie can schedule or monitor itself.',
        '- No inference, publication, external message or commerce action was performed by the observer.',
        '', '## Blocker and recovery', '',
    ])
    if status == 'COMPLETE':
        lines.append('- No deterministic health blocker was recorded. Sleep/wake behavior may still be untested.')
    else:
        lines.extend([
            '- Review each gap or failure before relying on this window as availability evidence.',
            '- Inspect the JSONL evidence, `yawdie status`, and the user LaunchAgent state.',
            '- Fix the identified local failure, preserve this evidence, then run a new bounded observation window.',
        ])
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = target.with_name('.' + target.name + '.tmp')
    temporary.write_text('\n'.join(lines) + '\n')
    os.chmod(temporary, 0o600)
    os.replace(temporary, target)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--logs', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--summary', type=Path, required=True)
    parser.add_argument('--start', required=True)
    parser.add_argument('--end', required=True)
    parser.add_argument('--interval', type=int, default=900)
    args = parser.parse_args()
    start = datetime.fromisoformat(args.start)
    end = datetime.fromisoformat(args.end)
    now = datetime.now(ZONE)
    if now < end:
        append_record(args.evidence, snapshot(args.database, args.logs, now))
    else:
        records = read_records(args.evidence)
        if not records or datetime.fromisoformat(records[-1]['observed_at']) < end:
            append_record(args.evidence, snapshot(args.database, args.logs, now))
            records = read_records(args.evidence)
        write_summary(args.summary, records, start, end, args.interval)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
