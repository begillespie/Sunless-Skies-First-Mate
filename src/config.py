#!/usr/bin/env python3
"""
@subsystem: engine_config
@version: 1.0.0
@file: src/config.py
@description: Zero-dependency .env loader and backend-agnostic BaseRepository factory
for Sunless Skies First Mate. Isolates datastore URIs and credentials from LLM tool schemas.
"""
from collections.abc import Callable
from dataclasses import dataclass, field
import os
from pathlib import Path

from src.exceptions import DatastoreError, ValidationError
from src.interfaces.repository import BaseRepository

DEFAULT_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
REPO_OPTION_PREFIX = "SUNLESS_SKIES_REPO_"

RepositoryFactory = Callable[["EngineConfig"], BaseRepository]
REPOSITORY_FACTORIES: dict[str, RepositoryFactory] = {}


def load_dotenv(env_path: str | Path | None = None, *, override: bool = False) -> dict[str, str]:
    """
    Loads KEY=VALUE pairs from a .env file into os.environ and returns the parsed mapping.
    Silently returns {} if the .env file does not exist (allowing process env vars alone).
    """
    path = Path(env_path) if env_path is not None else DEFAULT_ENV_PATH
    if not path.is_file():
        return {}

    parsed: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue

        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if not key:
            continue

        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]

        parsed[key] = val
        if override or key not in os.environ:
            os.environ[key] = val

    return parsed


@dataclass(frozen=True)
class EngineConfig:
    """Backend-agnostic datastore configuration loaded from .env / environment variables."""

    datastore_uri: str
    repository_backend: str = "google_sheets"
    options: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(cls, env_path: str | Path | None = None) -> "EngineConfig":
        """Loads .env and validates required datastore environment variables."""
        load_dotenv(env_path)
        datastore_uri = os.environ.get("SUNLESS_SKIES_DATASTORE_URI", "").strip()
        if not datastore_uri:
            raise DatastoreError(
                "SUNLESS_SKIES_DATASTORE_URI is not configured in .env or environment variables."
            )
        backend = (
            os.environ.get("SUNLESS_SKIES_REPOSITORY_BACKEND", "google_sheets").strip().lower()
            or "google_sheets"
        )
        options = {
            key[len(REPO_OPTION_PREFIX):].lower(): val
            for key, val in os.environ.items()
            if key.startswith(REPO_OPTION_PREFIX) and len(key) > len(REPO_OPTION_PREFIX)
        }
        return cls(
            datastore_uri=datastore_uri,
            repository_backend=backend,
            options=options,
        )


def register_repository_backend(name: str, factory: RepositoryFactory) -> None:
    """Registers a BaseRepository factory under a normalized backend key."""
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Repository backend name must be a non-empty string.")
    REPOSITORY_FACTORIES[name.strip().lower()] = factory


def _build_google_sheets_repo(config: EngineConfig) -> BaseRepository:
    """Lazy factory for the Google Sheets repository connector."""
    from src.connectors.google_sheets_repo import GoogleSheetsRepository

    return GoogleSheetsRepository(config.datastore_uri)


register_repository_backend("google_sheets", _build_google_sheets_repo)


def create_repository(
    config: EngineConfig | None = None,
    env_path: str | Path | None = None,
) -> BaseRepository:
    """Instantiates the configured BaseRepository backend without exposing credentials to the LLM."""
    resolved = config or EngineConfig.from_env(env_path)
    backend_key = resolved.repository_backend.strip().lower()
    factory = REPOSITORY_FACTORIES.get(backend_key)
    if factory is None:
        raise ValidationError(
            f"Unsupported repository backend: '{resolved.repository_backend}'. "
            f"Registered backends: {sorted(REPOSITORY_FACTORIES)}."
        )
    repo = factory(resolved)
    if not isinstance(repo, BaseRepository):
        raise ValidationError(
            f"Factory for backend '{backend_key}' returned {type(repo).__name__}, expected BaseRepository."
        )
    return repo
