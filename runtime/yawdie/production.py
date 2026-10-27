#!/usr/bin/env python3
"""Bounded recording-to-review adapter for Yawdie's authoritative SQLite queue."""
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path


CONTRACT_VERSION = '1.1.0'
ARCHITECTURE_VERSION = '1.0.0'
SOURCE_COMMIT = 'a18cac669e47e0dd489bffe8c7b3d2e74736b40c'
ADAPTER_VERSION = 'expertise-excerpt-1.0.0'
STAGES = ('submitted', 'intake', 'transcription', 'edit_preparation',
          'preview_render', 'QA', 'awaiting_review')
MAX_ATTEMPTS = 3
LEASE_SECONDS = 1800
ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.m4v'}
MAX_SOURCE_BYTES = 2_000_000_000


def sha256_file(path, chunk=1024 * 1024):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        while True:
            data = handle.read(chunk)
            if not data:
                break
            digest.update(data)
    return digest.hexdigest()


def initialize(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS production_acknowledgments (
        id TEXT PRIMARY KEY, contract_version TEXT NOT NULL,
        architecture_version TEXT NOT NULL, source_commit TEXT NOT NULL,
        implementation_commit TEXT NOT NULL, runtime_identity TEXT NOT NULL,
        acknowledged_at REAL NOT NULL);
      CREATE TABLE IF NOT EXISTS production_jobs (
        id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE NOT NULL,
        manifest_json TEXT NOT NULL, manifest_sha256 TEXT NOT NULL,
        status TEXT NOT NULL, submitted_at REAL NOT NULL, started_at REAL,
        completed_at REAL, current_stage TEXT NOT NULL, artifact_json TEXT,
        source_sha256 TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS production_stages (
        id TEXT PRIMARY KEY, job_id TEXT NOT NULL, name TEXT NOT NULL,
        ordinal INTEGER NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0,
        claimed_by TEXT, lease_token TEXT, lease_until REAL, started_at REAL,
        completed_at REAL, last_activity_at REAL, input_sha256 TEXT,
        output_sha256 TEXT, artifact TEXT, error_class TEXT,
        next_at REAL NOT NULL DEFAULT 0,
        UNIQUE(job_id, name));
      CREATE TABLE IF NOT EXISTS production_attempts (
        id TEXT PRIMARY KEY, job_id TEXT NOT NULL, stage_id TEXT NOT NULL,
        attempt_number INTEGER NOT NULL, worker_identity TEXT NOT NULL,
        pid INTEGER NOT NULL, started_at REAL NOT NULL, finished_at REAL,
        status TEXT NOT NULL, error_class TEXT, artifact TEXT);
    ''')
    columns = {row['name'] for row in db.execute('PRAGMA table_info(production_stages)')}
    if 'next_at' not in columns:
        db.execute('ALTER TABLE production_stages ADD COLUMN next_at REAL NOT NULL DEFAULT 0')


def _private_json(path):
    path = Path(path).expanduser().resolve(strict=True)
    if not path.is_file() or path.stat().st_mode & 0o077:
        raise ValueError('Production JSON files must be private regular files (0600)')
    return path, json.loads(path.read_text())


def load_config(path):
    path, data = _private_json(path)
    if data.get('schema_version') != 'yawdie-production-config-1':
        raise ValueError('Unsupported production config schema')
    roots = []
    for value in data.get('source_roots', []):
        root = Path(value).expanduser().resolve(strict=True)
        if not root.is_dir() or root.is_symlink():
            raise ValueError('Invalid source root')
        roots.append(root)
    if not roots:
        raise ValueError('At least one source root is required')
    output_root = Path(data['output_root']).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(output_root, 0o700)
    tools = {}
    for name in ('ffmpeg', 'ffprobe'):
        tool = Path(data['tools'][name]).resolve(strict=True)
        if not tool.is_file() or not os.access(tool, os.X_OK):
            raise ValueError('Configured tool is unavailable: ' + name)
        tools[name] = tool
    swift = Path(data['tools']['swift']).resolve(strict=True)
    if not swift.is_file() or not os.access(swift, os.X_OK):
        raise ValueError('Configured Swift runtime is unavailable')
    tools['swift'] = swift
    return {'path': path, 'source_roots': roots, 'output_root': output_root,
            'tools': tools, 'worker_identity': str(data.get('worker_identity', '')).strip()}


def _within(path, roots):
    resolved = Path(path).expanduser().resolve(strict=True)
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError('Source must be a regular non-symlink file')
    if not any(resolved == root or root in resolved.parents for root in roots):
        raise ValueError('Source is outside approved roots')
    if any(part.startswith('.') for part in resolved.parts):
        raise ValueError('Hidden source paths are not allowed')
    if resolved.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError('Unsupported source type')
    if resolved.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError('Source exceeds bounded size')
    return resolved


def acknowledge(db, implementation_commit, runtime_identity, now=None):
    initialize(db)
    now = time.time() if now is None else now
    if not re.fullmatch(r'[0-9a-f]{40}', implementation_commit):
        raise ValueError('Implementation commit must be a full Git SHA')
    if not runtime_identity or len(runtime_identity) > 160:
        raise ValueError('Runtime identity is required')
    ack_id = hashlib.sha256((CONTRACT_VERSION + '\0' + ARCHITECTURE_VERSION + '\0' +
                             SOURCE_COMMIT + '\0' + implementation_commit + '\0' +
                             runtime_identity).encode()).hexdigest()
    with db:
        db.execute('INSERT OR REPLACE INTO production_acknowledgments VALUES(?,?,?,?,?,?,?)',
                   (ack_id, CONTRACT_VERSION, ARCHITECTURE_VERSION, SOURCE_COMMIT,
                    implementation_commit, runtime_identity, now))
    return dict(db.execute('SELECT * FROM production_acknowledgments WHERE id=?', (ack_id,)).fetchone())


def acknowledgment(db):
    initialize(db)
    row = db.execute('SELECT * FROM production_acknowledgments ORDER BY acknowledged_at DESC LIMIT 1').fetchone()
    return dict(row) if row else None


def validate_manifest(config, data):
    required = {'schema_version', 'idempotency_key', 'episode', 'title', 'source',
                'source_sha256', 'start_seconds', 'end_seconds', 'style_version',
                'output_alias', 'review_required'}
    if set(data) - (required | {'instructions', 'protected_passages'}):
        raise ValueError('Manifest contains unsupported fields')
    if not required.issubset(data):
        raise ValueError('Manifest is missing required fields')
    if data['schema_version'] != 'yawdie-production-excerpt-1':
        raise ValueError('Unsupported manifest schema')
    if data['style_version'] != 'maim-captions-1.1.0':
        raise ValueError('Only the approved caption style is supported')
    if data['review_required'] is not True:
        raise ValueError('Founder review must remain required')
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{5,127}', data['idempotency_key']):
        raise ValueError('Invalid idempotency key')
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{2,80}', data['output_alias']):
        raise ValueError('Invalid output alias')
    start = float(data['start_seconds'])
    end = float(data['end_seconds'])
    if start < 0 or end <= start or end - start > 180:
        raise ValueError('Excerpt must be between 0 and 180 seconds')
    source = _within(data['source'], config['source_roots'])
    actual_hash = sha256_file(source)
    if not re.fullmatch(r'[0-9a-f]{64}', data['source_sha256']) or actual_hash != data['source_sha256']:
        raise ValueError('Source checksum mismatch')
    result = dict(data)
    result['source'] = str(source)
    result['start_seconds'] = start
    result['end_seconds'] = end
    return result


def submit(db, config_path, manifest_path, now=None):
    initialize(db)
    if not acknowledgment(db):
        raise ValueError('Production contract acknowledgment is required before submission')
    config = load_config(config_path)
    _, raw = _private_json(manifest_path)
    manifest = validate_manifest(config, raw)
    canonical = json.dumps(manifest, sort_keys=True, separators=(',', ':'))
    manifest_hash = hashlib.sha256(canonical.encode()).hexdigest()
    job_id = uuid.uuid4().hex
    now = time.time() if now is None else now
    with db:
        inserted = db.execute(
            'INSERT OR IGNORE INTO production_jobs VALUES(?,?,?,?,?,?,?,?,?,?,?)',
            (job_id, manifest['idempotency_key'], canonical, manifest_hash, 'queued', now,
             None, None, 'submitted', None, manifest['source_sha256'])).rowcount
        row = db.execute('SELECT * FROM production_jobs WHERE idempotency_key=?',
                         (manifest['idempotency_key'],)).fetchone()
        if inserted:
            for ordinal, name in enumerate(STAGES):
                status = 'completed' if name == 'submitted' else ('queued' if name == 'intake' else 'pending')
                db.execute('INSERT INTO production_stages(id,job_id,name,ordinal,status,completed_at,last_activity_at,input_sha256) '
                           'VALUES(?,?,?,?,?,?,?,?)',
                           (uuid.uuid4().hex, job_id, name, ordinal, status,
                            now if name == 'submitted' else None, now, manifest_hash))
    return {'job_id': row['id'], 'status': row['status'], 'duplicate': not bool(inserted),
            'manifest_sha256': row['manifest_sha256']}


def _run(argv, timeout, output_limit=200000, cwd=None, env=None):
    result = subprocess.run([str(item) for item in argv], shell=False, capture_output=True,
                            timeout=timeout, cwd=cwd, env=env)
    if result.returncode:
        raise RuntimeError('bounded tool failed with exit code ' + str(result.returncode))
    return result.stdout[:output_limit]


def _probe(config, path):
    out = _run([config['tools']['ffprobe'], '-v', 'error', '-show_entries',
                'format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate',
                '-of', 'json', path], 60)
    return json.loads(out)


def _srt_time(value):
    hours, minutes, rest = value.replace('.', ',').split(':')
    seconds, millis = rest.split(',')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000


def _ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int(seconds % 3600 // 60)
    whole = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    return f'{hours}:{minutes:02d}:{whole:02d}.{centis:02d}'


def srt_to_active_word_ass(srt_text):
    header = '''[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: MAIM,Arial,58,&H00FFFFFF,&H0000C8FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,2,120,120,90,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
    events = []
    blocks = re.split(r'\n\s*\n', srt_text.strip())
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next((i for i, line in enumerate(lines) if '-->' in line), None)
        if timing_index is None:
            continue
        start_text, end_text = [part.strip().split()[0] for part in lines[timing_index].split('-->')]
        start, end = _srt_time(start_text), _srt_time(end_text)
        text = ' '.join(lines[timing_index + 1:]).replace('{', '(').replace('}', ')')
        words = text.split()
        if not words or end <= start:
            continue
        events.append(f'Dialogue: 0,{_ass_time(start)},{_ass_time(end)},MAIM,,0,0,0,,{text}')
        span = (end - start) / len(words)
        for index in range(len(words)):
            pieces = []
            for position, word in enumerate(words):
                if position == index:
                    pieces.append(r'{\c&H0000C8FF&\alpha&H00&}' + word)
                else:
                    pieces.append(r'{\alpha&HFF&}' + word)
            active_start = start + span * index
            active_end = start + span * (index + 1)
            events.append(f'Dialogue: 1,{_ass_time(active_start)},{_ass_time(active_end)},MAIM,,0,0,0,,{" ".join(pieces)}')
    if not events:
        raise ValueError('No usable caption cues were found')
    return header + '\n'.join(events) + '\n'


def srt_to_cues(srt_text):
    cues = []
    for block in re.split(r'\n\s*\n', srt_text.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next((i for i, line in enumerate(lines) if '-->' in line), None)
        if timing_index is None:
            continue
        start_text, end_text = [part.strip().split()[0] for part in lines[timing_index].split('-->')]
        text = ' '.join(lines[timing_index + 1:]).replace('<i>', '').replace('</i>', '').strip()
        if text:
            cues.append({'start': _srt_time(start_text), 'end': _srt_time(end_text), 'text': text})
    if not cues:
        raise ValueError('No usable caption cues were found')
    return cues


def _job_dir(config, job_id):
    target = config['output_root'] / job_id
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(target, 0o700)
    return target


def _atomic_json(path, data):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True))
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    os.chmod(path, 0o600)


def _execute_stage(db, config, job, stage):
    manifest = json.loads(job['manifest_json'])
    folder = _job_dir(config, job['job_id'])
    name = stage['name']
    source = Path(manifest['source'])
    if name == 'intake':
        probe = _probe(config, source)
        streams = {item.get('codec_type') for item in probe.get('streams', [])}
        duration = float(probe.get('format', {}).get('duration', 0))
        if not {'video', 'audio', 'subtitle'}.issubset(streams):
            raise ValueError('Source requires video, audio and subtitle streams')
        if duration < manifest['end_seconds']:
            raise ValueError('Source is shorter than requested excerpt')
        path = folder / 'intake.json'
        _atomic_json(path, {'source_sha256': manifest['source_sha256'], 'bytes': source.stat().st_size,
                            'duration': duration, 'streams': sorted(streams), 'adapter': ADAPTER_VERSION})
        return path
    if name == 'transcription':
        path = folder / 'captions.srt'
        tmp = folder / 'captions.srt.tmp'
        _run([config['tools']['ffmpeg'], '-nostdin', '-y', '-i', source,
              '-ss', manifest['start_seconds'], '-t', manifest['end_seconds'] - manifest['start_seconds'],
              '-map', '0:s:0', '-c:s', 'srt',
              '-f', 'srt', tmp], 180)
        if not tmp.exists() or tmp.stat().st_size == 0:
            raise ValueError('Embedded transcript extraction produced no captions')
        os.replace(tmp, path)
        os.chmod(path, 0o600)
        return path
    if name == 'edit_preparation':
        srt = folder / 'captions.srt'
        path = folder / 'captions-active-word.ass'
        tmp = path.with_suffix('.ass.tmp')
        tmp.write_text(srt_to_active_word_ass(srt.read_text()))
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
        props = folder / 'render-props.json'
        _atomic_json(props, {'source': str(source), 'startSeconds': manifest['start_seconds'],
                             'durationSeconds': manifest['end_seconds'] - manifest['start_seconds'],
                             'cues': srt_to_cues(srt.read_text())})
        return path
    if name == 'preview_render':
        path = folder / (manifest['output_alias'] + '.mp4')
        tmp = folder / (manifest['output_alias'] + '.tmp.mp4')
        renderer = Path(__file__).resolve().parent / 'render_excerpt.swift'
        props = folder / 'render-props.json'
        if not props.exists():
            _atomic_json(props, {'source': str(source), 'startSeconds': manifest['start_seconds'],
                                 'durationSeconds': manifest['end_seconds'] - manifest['start_seconds'],
                                 'cues': srt_to_cues((folder / 'captions.srt').read_text())})
        _run([config['tools']['swift'], renderer, props, tmp], 1800)
        os.replace(tmp, path)
        os.chmod(path, 0o600)
        return path
    if name == 'QA':
        preview = folder / (manifest['output_alias'] + '.mp4')
        probe = _probe(config, preview)
        streams = {item.get('codec_type') for item in probe.get('streams', [])}
        duration = float(probe.get('format', {}).get('duration', 0))
        expected = manifest['end_seconds'] - manifest['start_seconds']
        passed = {'video', 'audio'}.issubset(streams) and abs(duration - expected) <= 2
        path = folder / 'qa.json'
        findings = {
            'technical_pass': passed, 'creative_review': 'required',
            'duration_seconds': duration, 'expected_seconds': expected,
            'streams': sorted(streams), 'caption_file_present': (folder / 'captions-active-word.ass').exists(),
            'caption_style': 'white, thin black outline, gold active word',
            'render_engine': 'AVFoundation/CoreAnimation via pinned adapter source',
            'sync_status': 'derived from embedded subtitle timings; human listening review required',
            'preview_sha256': sha256_file(preview), 'preview_bytes': preview.stat().st_size,
        }
        _atomic_json(path, findings)
        if not passed:
            raise ValueError('Technical QA failed')
        return path
    if name == 'awaiting_review':
        preview = folder / (manifest['output_alias'] + '.mp4')
        packet = folder / 'evidence.json'
        _atomic_json(packet, {'status': 'finalizing_receipts', 'job_id': job['job_id']})
        return packet
    raise ValueError('Unsupported production stage')


def _claim(db, identity, now=None):
    now = time.time() if now is None else now
    db.execute('BEGIN IMMEDIATE')
    try:
        expired = db.execute("SELECT * FROM production_stages WHERE status='running' AND lease_until<=?", (now,)).fetchall()
        for row in expired:
            status = 'blocked' if row['attempts'] >= MAX_ATTEMPTS else 'queued'
            db.execute('UPDATE production_stages SET status=?,lease_token=NULL,lease_until=NULL,error_class=?,next_at=? WHERE id=?',
                       (status, 'lease_expired', now, row['id']))
            db.execute("UPDATE production_attempts SET finished_at=?,status='lease_expired',error_class='lease_expired' "
                       'WHERE id=? AND finished_at IS NULL', (now, row['lease_token']))
        row = db.execute("SELECT s.*,j.manifest_json,j.manifest_sha256,j.source_sha256,j.status job_status,j.submitted_at "
                         "FROM production_stages s JOIN production_jobs j ON j.id=s.job_id "
                         "WHERE s.status='queued' AND s.next_at<=? ORDER BY j.submitted_at,s.ordinal LIMIT 1",
                         (now,)).fetchone()
        if not row:
            db.commit()
            return None
        token = uuid.uuid4().hex
        attempt = row['attempts'] + 1
        db.execute("UPDATE production_stages SET status='running',attempts=?,claimed_by=?,lease_token=?,lease_until=?,"
                   'started_at=COALESCE(started_at,?),last_activity_at=? WHERE id=? AND status=\'queued\'',
                   (attempt, identity, token, now + LEASE_SECONDS, now, now, row['id']))
        db.execute('INSERT INTO production_attempts VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                   (token, row['job_id'], row['id'], attempt, identity, os.getpid(), now, None, 'running', None, None))
        db.execute("UPDATE production_jobs SET status='running',started_at=COALESCE(started_at,?),current_stage=? WHERE id=?",
                   (now, row['name'], row['job_id']))
        result = dict(db.execute('SELECT s.*,j.manifest_json,j.manifest_sha256,j.source_sha256,j.status job_status,j.submitted_at '
                                 'FROM production_stages s JOIN production_jobs j ON j.id=s.job_id WHERE s.id=?',
                                 (row['id'],)).fetchone())
        db.commit()
        return result
    except BaseException:
        db.rollback()
        raise


def _complete(db, stage, artifact, now=None):
    now = time.time() if now is None else now
    output_hash = sha256_file(artifact)
    with db:
        changed = db.execute("UPDATE production_stages SET status='completed',completed_at=?,last_activity_at=?,"
                             'output_sha256=?,artifact=?,lease_token=NULL,lease_until=NULL,next_at=0 WHERE id=? AND status=\'running\' AND lease_token=?',
                             (now, now, output_hash, str(artifact), stage['id'], stage['lease_token'])).rowcount
        if not changed:
            return False
        db.execute("UPDATE production_attempts SET finished_at=?,status='completed',artifact=? WHERE id=?",
                   (now, str(artifact), stage['lease_token']))
        next_row = db.execute('SELECT * FROM production_stages WHERE job_id=? AND ordinal>? ORDER BY ordinal LIMIT 1',
                              (stage['job_id'], stage['ordinal'])).fetchone()
        if next_row:
            db.execute("UPDATE production_stages SET status='queued',input_sha256=?,last_activity_at=? WHERE id=?",
                       (output_hash, now, next_row['id']))
            db.execute('UPDATE production_jobs SET current_stage=? WHERE id=?', (next_row['name'], stage['job_id']))
        else:
            db.execute("UPDATE production_jobs SET status='awaiting_review',completed_at=?,current_stage='awaiting_review',artifact_json=? WHERE id=?",
                       (now, json.dumps({'evidence': str(artifact)}), stage['job_id']))
    return True


def _fail(db, stage, exc, now=None):
    now = time.time() if now is None else now
    error_class = type(exc).__name__
    retryable = isinstance(exc, (subprocess.TimeoutExpired, RuntimeError))
    status = 'queued' if retryable and stage['attempts'] < MAX_ATTEMPTS else 'blocked'
    next_at = now + 60 * (2 ** max(stage['attempts'] - 1, 0)) if status == 'queued' else now
    with db:
        db.execute('UPDATE production_stages SET status=?,last_activity_at=?,error_class=?,next_at=?,lease_token=NULL,lease_until=NULL '
                   'WHERE id=? AND lease_token=?', (status, now, error_class, next_at, stage['id'], stage['lease_token']))
        db.execute('UPDATE production_attempts SET finished_at=?,status=?,error_class=? WHERE id=?',
                   (now, status, error_class, stage['lease_token']))
        db.execute('UPDATE production_jobs SET status=?,current_stage=? WHERE id=?',
                   ('blocked' if status == 'blocked' else 'queued', stage['name'], stage['job_id']))


def release_for_service_stop(db, stage, now=None):
    now = time.time() if now is None else now
    with db:
        changed = db.execute("UPDATE production_stages SET status='queued',attempts=MAX(attempts-1,0),"
                             'last_activity_at=?,next_at=0,lease_token=NULL,lease_until=NULL,error_class=\'administrative_interrupt\' '
                             "WHERE id=? AND status='running' AND lease_token=?",
                             (now, stage['id'], stage['lease_token'])).rowcount
        if changed:
            db.execute("UPDATE production_attempts SET finished_at=?,status='administrative_interrupt',"
                       "error_class='administrative_interrupt' WHERE id=?", (now, stage['lease_token']))
            db.execute("UPDATE production_jobs SET status='queued' WHERE id=?", (stage['job_id'],))
    return bool(changed)


def run_once(db, config_path, now=None):
    initialize(db)
    config = load_config(config_path)
    identity = config['worker_identity'] or ('launchagent:' + str(os.getuid()))
    stage = _claim(db, identity, now)
    if not stage:
        return False
    try:
        artifact = _execute_stage(db, config, stage, stage)
        _complete(db, stage, artifact, now)
        if stage['name'] == 'awaiting_review':
            finalize_evidence(db, config, stage['job_id'])
    except Exception as exc:
        if type(exc).__name__ == 'ServiceStop':
            release_for_service_stop(db, stage, now)
            raise
        _fail(db, stage, exc, now)
    return True


def finalize_evidence(db, config, job_id):
    job = db.execute('SELECT * FROM production_jobs WHERE id=?', (job_id,)).fetchone()
    manifest = json.loads(job['manifest_json'])
    folder = _job_dir(config, job_id)
    preview = folder / (manifest['output_alias'] + '.mp4')
    packet = folder / 'evidence.json'
    attempts = [dict(row) for row in db.execute(
        'SELECT id,stage_id,attempt_number,worker_identity,pid,started_at,finished_at,status,error_class,artifact '
        'FROM production_attempts WHERE job_id=? ORDER BY started_at', (job_id,))]
    stages = [dict(row) for row in db.execute(
        'SELECT id,name,status,attempts,claimed_by,started_at,completed_at,last_activity_at,input_sha256,output_sha256,artifact,error_class '
        'FROM production_stages WHERE job_id=? ORDER BY ordinal', (job_id,))]
    _atomic_json(packet, {'status': 'awaiting_review', 'job_id': job_id, 'adapter': ADAPTER_VERSION,
                          'contract_version': CONTRACT_VERSION, 'architecture_version': ARCHITECTURE_VERSION,
                          'source_commit': SOURCE_COMMIT, 'source_sha256': manifest['source_sha256'],
                          'preview': str(preview), 'preview_bytes': preview.stat().st_size,
                          'preview_sha256': sha256_file(preview), 'stages': stages, 'attempts': attempts,
                          'manual_steps': ['Watch the excerpt for word sync, legibility and safe placement.',
                                           'Approve or request changes; publishing remains out of scope.']})
    digest = sha256_file(packet)
    with db:
        db.execute("UPDATE production_stages SET output_sha256=? WHERE job_id=? AND name='awaiting_review'",
                   (digest, job_id))
        db.execute("UPDATE production_jobs SET artifact_json=? WHERE id=?",
                   (json.dumps({'evidence': str(packet), 'evidence_sha256': digest}), job_id))
    return packet


def report(db, job_id=None):
    initialize(db)
    clause, params = ('WHERE id=?', (job_id,)) if job_id else ('ORDER BY submitted_at DESC LIMIT 20', ())
    rows = db.execute('SELECT * FROM production_jobs ' + clause, params).fetchall()
    jobs = []
    for row in rows:
        item = dict(row)
        item['manifest_json'] = json.loads(item['manifest_json'])
        item['stages'] = [dict(value) for value in db.execute(
            'SELECT id,name,ordinal,status,attempts,claimed_by,started_at,completed_at,last_activity_at,input_sha256,output_sha256,artifact,error_class '
            'FROM production_stages WHERE job_id=? ORDER BY ordinal', (row['id'],))]
        item['attempts'] = [dict(value) for value in db.execute(
            'SELECT id,stage_id,attempt_number,worker_identity,pid,started_at,finished_at,status,error_class,artifact '
            'FROM production_attempts WHERE job_id=? ORDER BY started_at', (row['id'],))]
        jobs.append(item)
    return {'acknowledgment': acknowledgment(db), 'jobs': jobs}

