#!/usr/bin/env python3
"""Major OS Markdown bridge. SQLite remains the execution authority."""
import hashlib
import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path, PurePosixPath
from zoneinfo import ZoneInfo

import worker
from path_policy import PathPolicy, PathPolicyError, TemporarilyUnavailable

VAULT_DIRS = (
    'Yawdie/Context',
    'Yawdie/Briefs/Inbox',
    'Yawdie/Reports',
    'Yawdie/Templates',
)
READ_DIRS = ('Yawdie/Context', 'Yawdie/Briefs/Inbox')
MAX_CONTEXT_BYTES = 12000
MAX_CONTEXT_FILES = 16
MAX_CONTEXT_FILE_BYTES = 4000


def policy(vault_root, max_file_bytes=65536):
    return PathPolicy(vault_root, VAULT_DIRS, suffixes=('.md',), max_file_bytes=max_file_bytes)


def initialize_layout(vault_root):
    supplied = Path(vault_root).expanduser()
    if supplied.is_symlink():
        raise PathPolicyError('vault root cannot be a symlink')
    root = supplied.resolve(strict=True)
    created = []
    for relative in VAULT_DIRS:
        target = root / relative
        if target.exists() and (target.is_symlink() or not target.is_dir()):
            raise PathPolicyError('vault layout target must be a real directory')
        if not target.exists():
            target.mkdir(parents=True, mode=0o700)
            created.append(relative)
    return created


def load_context(vault_root):
    reader = policy(vault_root, MAX_CONTEXT_FILE_BYTES)
    parts = []
    provenance = []
    used = 0
    unavailable = []
    rejected = []
    try:
        candidates = reader.markdown_files('Yawdie/Context')
        for relative in candidates:
            if len(provenance) >= MAX_CONTEXT_FILES:
                break
            try:
                item = reader.read_text(relative)
            except TemporarilyUnavailable:
                unavailable.append(relative)
                continue
            except PathPolicyError:
                rejected.append(relative)
                continue
            encoded = item['text'].encode('utf-8')
            remaining = MAX_CONTEXT_BYTES - used
            if remaining <= 0:
                break
            included = encoded[:remaining].decode('utf-8', errors='ignore')
            if not included:
                break
            parts.append('CONTEXT FILE ' + relative + '\n' + included)
            used += len(included.encode('utf-8'))
            provenance.append({key: item[key] for key in ('relative_path', 'sha256', 'bytes')})
    except TemporarilyUnavailable:
        unavailable.append('Yawdie/Context')
    text = '\n\n'.join(parts)
    return {
        'text': text,
        'sha256': hashlib.sha256(text.encode()).hexdigest(),
        'bytes': used,
        'files': provenance,
        'unavailable': unavailable,
        'rejected': rejected,
        'truncated': used >= MAX_CONTEXT_BYTES or len(provenance) >= MAX_CONTEXT_FILES,
    }


def _task(body):
    match = re.search(r'(?mi)^Yawdie-Task:\s*([a-z-]+)\s*$', body)
    return match.group(1) if match else 'source-to-draft'


def submit(db, vault_root, source, day=None, rerun=False):
    reader = policy(vault_root)
    item = reader.read_text(source)
    relative = PurePosixPath(item['relative_path'])
    if not relative.is_relative_to(PurePosixPath('Yawdie/Briefs/Inbox')):
        raise PathPolicyError('brief must be inside Yawdie/Briefs/Inbox')
    if not worker.watcher_actionable(Path(relative.name), item['text']):
        raise ValueError('brief is not actionable or is a template')
    task = _task(item['text'])
    if task not in worker.TASK_FIELDS:
        raise ValueError('blocked: adapter unavailable')
    context = load_context(vault_root)
    day = day or datetime.now(ZoneInfo('Asia/Makassar')).date().isoformat()
    reference = 'obsidian:' + item['relative_path']
    job_id = worker.enqueue(db, 'maim', item['text'], reference, day, task, rerun)
    with db:
        db.execute(
            'INSERT OR IGNORE INTO job_contexts(job_id,context_sha256,context_text,provenance) VALUES(?,?,?,?)',
            (job_id, context['sha256'], context['text'], json.dumps({
                'brief': {key: item[key] for key in ('relative_path', 'sha256', 'bytes')},
                'context': context['files'],
                'context_bytes': context['bytes'],
                'context_truncated': context['truncated'],
                'temporarily_unavailable': context['unavailable'],
                'rejected_context': context['rejected'],
            }, sort_keys=True)))
    return {
        'job_id': job_id,
        'task': task,
        'intentional_rerun': rerun,
        'source': {key: item[key] for key in ('relative_path', 'sha256', 'bytes')},
        'context': {key: context[key] for key in ('sha256', 'bytes', 'files', 'unavailable', 'rejected', 'truncated')},
    }


def scan(db, vault_root, day=None):
    reader = policy(vault_root)
    receipts = []
    unavailable = []
    blocked = []
    try:
        candidates = list(reader.markdown_files('Yawdie/Briefs/Inbox'))
    except TemporarilyUnavailable:
        return {'submitted': receipts, 'temporarily_unavailable': ['Yawdie/Briefs/Inbox'], 'blocked': blocked}
    for relative in candidates:
        try:
            _, candidate = reader.resolve(relative)
            try:
                stat = candidate.stat()
            except OSError as exc:
                raise TemporarilyUnavailable('brief is temporarily unavailable') from exc
            previous = db.execute(
                'SELECT mtime_ns,size FROM vault_files WHERE path=?', (relative,)).fetchone()
            if previous and previous['mtime_ns'] == stat.st_mtime_ns and previous['size'] == stat.st_size:
                continue
            item = reader.read_text(relative)
        except TemporarilyUnavailable:
            unavailable.append(relative)
            continue
        with db:
            db.execute('INSERT OR REPLACE INTO vault_files VALUES(?,?,?,?,?)',
                       (relative, stat.st_mtime_ns, stat.st_size, item['sha256'], datetime.now().timestamp()))
        if not worker.watcher_actionable(Path(relative), item['text']):
            continue
        try:
            receipts.append(submit(db, vault_root, relative, day=day))
        except TemporarilyUnavailable:
            unavailable.append(relative)
        except (ValueError, PathPolicyError) as exc:
            reason = 'adapter unavailable' if 'adapter unavailable' in str(exc) else type(exc).__name__
            blocked.append({'source': relative, 'reason': reason})
    return {'submitted': receipts, 'temporarily_unavailable': unavailable, 'blocked': blocked}


def _markdown(packet, attempts, provenance):
    draft = packet['draft']
    source_note = '[[' + provenance['brief']['relative_path'][:-3] + ']]'
    lines = [
        '---',
        'title: ' + json.dumps('Yawdie Report ' + packet['job_id']),
        'date: ' + packet['day'],
        'tags:',
        '  - yawdie/report',
        'status: ' + packet['status'],
        'job_id: ' + packet['job_id'],
        'task: ' + packet['task'],
        'model: ' + json.dumps(packet['model']),
        'source_note: ' + json.dumps(source_note),
        'source_sha256: ' + provenance['brief']['sha256'],
        'context_sha256: ' + packet.get('context_sha256', ''),
        '---', '',
        '# Yawdie Report', '',
        f"- Job ID: `{packet['job_id']}`",
        f"- Status: `{packet['status']}`",
        f"- Task: `{packet['task']}`",
        f"- Model: `{packet['model']}`",
        f"- Source: `{provenance['brief']['relative_path']}`",
        f"- Source SHA-256: `{provenance['brief']['sha256']}`",
        f"- Context SHA-256: `{packet.get('context_sha256', '')}`",
        f"- Attempts: `{len(attempts)}`",
        f"- Inference duration: `{packet.get('inference', {}).get('total_duration', 0) / 1_000_000_000:.3f} seconds`",
        '', '## Draft', '',
    ]
    for field, value in draft.items():
        lines.extend(['### ' + field.replace('_', ' ').title(), '', str(value), ''])
    lines.extend(['## Context provenance', ''])
    if provenance['context']:
        for item in provenance['context']:
            lines.append(f"- `{item['relative_path']}` — `{item['sha256']}` ({item['bytes']} bytes)")
    else:
        lines.append('- No context files loaded.')
    if provenance.get('temporarily_unavailable'):
        lines.extend(['', '## Temporarily unavailable', ''])
        lines.extend('- `' + item + '`' for item in provenance['temporarily_unavailable'])
    if provenance.get('rejected_context'):
        lines.extend(['', '## Rejected context', ''])
        lines.extend('- `' + item + '` — rejected by path policy' for item in provenance['rejected_context'])
    lines.extend([
        '', '## Boundaries', '',
        '> [!warning] Drafting boundary',
        '> - Publishing: blocked: adapter unavailable',
        '> - External messages: blocked: adapter unavailable',
        '> - Commerce: blocked: adapter unavailable',
        '> - This is completed drafting only; no external action was performed.',
        '', '## Execution evidence', '',
    ])
    for attempt in attempts:
        lines.append(f"- Attempt {attempt['attempt_number']}: `{attempt['status']}`; failure `{attempt['failure_class'] or 'none'}`")
    return '\n'.join(lines) + '\n'


def export_report(db, vault_root, job_id):
    row = db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
    if not row:
        raise ValueError('unknown job')
    if row['status'] != 'draft_ready' or not row['artifact']:
        raise ValueError('job is not ready for report export')
    context_row = db.execute('SELECT * FROM job_contexts WHERE job_id=?', (job_id,)).fetchone()
    if not context_row:
        raise ValueError('job has no vault provenance')
    packet = json.loads(Path(row['artifact']).read_text())
    packet['context_sha256'] = context_row['context_sha256']
    provenance = json.loads(context_row['provenance'])
    attempts = [dict(item) for item in db.execute(
        'SELECT attempt_number,status,failure_class FROM execution_attempts WHERE job_id=? ORDER BY started_at',
        (job_id,))]
    content = _markdown(packet, attempts, provenance)
    reader = policy(vault_root)
    _, reports = reader.resolve('Yawdie/Reports', require_file=False)
    destination = reports / (job_id + '.md')
    if destination.is_symlink():
        raise PathPolicyError('report destination cannot be a symlink')
    if destination.exists():
        try:
            existing = destination.read_text()
        except OSError as exc:
            raise TemporarilyUnavailable('report is temporarily unavailable') from exc
        if existing == content:
            with db:
                db.execute('INSERT OR REPLACE INTO vault_exports VALUES(?,?,?)',
                           (job_id, 'Yawdie/Reports/' + destination.name, datetime.now().timestamp()))
            return {'job_id': job_id, 'report': 'Yawdie/Reports/' + destination.name, 'unchanged': True}
        raise FileExistsError('report already exists; founder notes are never overwritten')
    temporary = reports / ('.' + job_id + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temporary.open('x', encoding='utf-8') as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, destination)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise TemporarilyUnavailable('report folder is temporarily unavailable') from exc
    report = 'Yawdie/Reports/' + destination.name
    with db:
        db.execute('INSERT OR REPLACE INTO vault_exports VALUES(?,?,?)',
                   (job_id, report, datetime.now().timestamp()))
    return {'job_id': job_id, 'report': report, 'unchanged': False}


def export_ready(db, vault_root):
    exported = []
    unavailable = []
    blocked = []
    rows = db.execute(
        "SELECT j.id FROM jobs j JOIN job_contexts c ON c.job_id=j.id "
        "LEFT JOIN vault_exports e ON e.job_id=j.id "
        "WHERE j.status='draft_ready' AND e.job_id IS NULL ORDER BY j.rowid").fetchall()
    for row in rows:
        try:
            exported.append(export_report(db, vault_root, row['id']))
        except TemporarilyUnavailable:
            unavailable.append(row['id'])
        except (FileExistsError, ValueError, PathPolicyError) as exc:
            blocked.append({'job_id': row['id'], 'reason': type(exc).__name__})
    return {'exported': exported, 'temporarily_unavailable': unavailable, 'blocked': blocked}


def cycle(db, vault_root, day=None):
    """One non-destructive intake/export cycle for an optional supervised loop."""
    return {'scan': scan(db, vault_root, day), 'reports': export_ready(db, vault_root)}
