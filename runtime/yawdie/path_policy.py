#!/usr/bin/env python3
"""Bounded, allowlisted local-file access for Yawdie adapters."""
import hashlib
import os
from pathlib import Path, PurePosixPath


class PathPolicyError(ValueError):
    """A requested path is outside the approved local-file contract."""


class TemporarilyUnavailable(OSError):
    """A permitted iCloud/local file could not be read at this time."""


class PathPolicy:
    def __init__(self, root, allowed_roots, suffixes=('.md',), max_file_bytes=65536):
        supplied = Path(root).expanduser()
        if supplied.is_symlink():
            raise PathPolicyError('approved root cannot be a symlink')
        self.root = supplied.resolve(strict=True)
        if not self.root.is_dir():
            raise PathPolicyError('approved root must be a directory')
        self.allowed_roots = tuple(PurePosixPath(value) for value in allowed_roots)
        if not self.allowed_roots or any(p.is_absolute() or '..' in p.parts for p in self.allowed_roots):
            raise PathPolicyError('allowed roots must be relative and bounded')
        self.suffixes = frozenset(value.lower() for value in suffixes)
        self.max_file_bytes = max_file_bytes

    @staticmethod
    def _relative(value):
        raw = str(value).replace(os.sep, '/')
        relative = PurePosixPath(raw)
        if relative.is_absolute() or '..' in relative.parts or not relative.parts:
            raise PathPolicyError('path traversal or absolute paths are not allowed')
        if any(part.startswith('.') for part in relative.parts):
            raise PathPolicyError('hidden and plugin paths are not allowed')
        return relative

    def _is_allowed(self, relative):
        return any(relative == base or relative.is_relative_to(base) for base in self.allowed_roots)

    def resolve(self, value, require_file=True):
        relative = self._relative(value)
        if not self._is_allowed(relative):
            raise PathPolicyError('path is outside approved roots')
        candidate = self.root.joinpath(*relative.parts)
        current = self.root
        for part in relative.parts:
            current = current / part
            try:
                if current.is_symlink():
                    raise PathPolicyError('symlink paths are not allowed')
            except OSError as exc:
                raise TemporarilyUnavailable('approved path is temporarily unavailable') from exc
        try:
            resolved = candidate.resolve(strict=True)
        except (FileNotFoundError, OSError) as exc:
            raise TemporarilyUnavailable('approved path is temporarily unavailable') from exc
        if self.root not in resolved.parents and resolved != self.root:
            raise PathPolicyError('resolved path escaped approved root')
        if require_file and not resolved.is_file():
            raise PathPolicyError('approved path is not a file')
        return relative, resolved

    def read_text(self, value):
        relative, path = self.resolve(value)
        if path.suffix.lower() not in self.suffixes:
            raise PathPolicyError('file type is not approved')
        try:
            size = path.stat().st_size
            if size > self.max_file_bytes:
                raise PathPolicyError('file exceeds size limit')
            data = path.read_bytes()
        except PathPolicyError:
            raise
        except OSError as exc:
            raise TemporarilyUnavailable('approved file is temporarily unavailable') from exc
        if b'\x00' in data:
            raise PathPolicyError('binary files are not allowed')
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise PathPolicyError('file must be UTF-8 text') from exc
        return {
            'relative_path': relative.as_posix(),
            'text': text,
            'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data),
        }

    def markdown_files(self, relative_root):
        relative, directory = self.resolve(relative_root, require_file=False)
        if not directory.is_dir():
            raise PathPolicyError('approved scan root is not a directory')
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name.casefold())
        except OSError as exc:
            raise TemporarilyUnavailable('approved folder is temporarily unavailable') from exc
        for path in entries:
            if path.name.startswith('.') or path.is_symlink() or not path.is_file():
                continue
            child = relative / path.name
            if path.suffix.lower() in self.suffixes:
                yield child.as_posix()
