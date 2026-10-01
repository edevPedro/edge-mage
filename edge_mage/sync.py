"""Offline-first catalog + progress sync stubs (MAGE_API_BASE).

Endpoints (edevs):
  GET/POST {base}/api/estudo/mage/progress
  Optional catalog → ~/.mage/packs/
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from edge_mage.auth import api_base, load_auth
from edge_mage.paths import packs_dir, progress_path


@dataclass
class SyncResult:
    ok: bool
    message: str
    pulled: bool = False
    pushed: bool = False
    warning: str = ""


def _auth_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "e-mage-tui/0.2",
    }
    auth = load_auth()
    token = auth.get("github_token") or os.environ.get("MAGE_TOKEN") or ""
    if token:
        headers["Authorization"] = f"Bearer {token}"
    # edevs mage-api may also accept X-Mage-Key
    key = os.environ.get("MAGE_API_KEY", "").strip()
    if key:
        headers["X-Mage-Key"] = key
    return headers


def _http_json(
    method: str, url: str, body: dict[str, Any] | None = None
) -> tuple[int, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = Request(url, data=data, headers=_auth_headers(), method=method)
    try:
        with urlopen(req, timeout=20) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except Exception:
            payload = {"error": str(exc)}
        return exc.code, payload
    except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return 0, {"error": str(exc)}


def progress_to_api_payload(progress: dict[str, Any], *, user: str = "pedro") -> dict:
    """
    Adapt local TUI progress.json to the edevs mage progress shape.

    Existing API expects { readAt, activeDays } for full sync, or { articleId }.
    We map completed room_ids → readAt timestamps and include a `tui` blob
    for future servers that understand the full TUI state.
    """
    read_at: dict[str, str] = {}
    now = datetime.now(timezone.utc).isoformat()

    global_rooms = progress.get("completed_rooms_by_id") or {}
    for room_id, done in global_rooms.items():
        if done:
            read_at[str(room_id)] = now

    # also map track/room keys
    for key, done in (progress.get("completed_rooms") or {}).items():
        if done:
            room_id = str(key).rsplit("/", 1)[-1]
            read_at.setdefault(room_id, now)

    active = progress.get("active_days")
    if not isinstance(active, list) or not active:
        last = progress.get("last_active") or date.today().isoformat()
        active = [str(last)]

    return {
        "user": user,
        "readAt": read_at,
        "activeDays": [str(d) for d in active],
        "tui": {
            "xp": progress.get("xp", 0),
            "completed_rooms": progress.get("completed_rooms", {}),
            "completed_rooms_by_id": progress.get("completed_rooms_by_id", {}),
            "courses": progress.get("courses", {}),
            "rituals": progress.get("rituals", {}),
            "global_rank": progress.get("global_rank"),
            "version": progress.get("version", 4),
        },
    }


def pull_catalog(*, course: str = "systems") -> SyncResult:
    """Pull catalog JSON into ~/.mage/packs/<course>.json (stub-friendly)."""
    packs = packs_dir()
    dest = packs / f"{course}.json"
    base = api_base()
    url = f"{base}/api/estudo/mage/catalog?course={course}"
    status, data = _http_json("GET", url)
    if status == 200 and isinstance(data, dict):
        dest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return SyncResult(ok=True, message=f"catalog → {dest}", pulled=True)

    # Offline stub: ensure a minimal pack exists for systems
    if not dest.exists():
        stub = {
            "course": course,
            "stub": True,
            "rooms": [
                {
                    "id": "flag-hello",
                    "title": "FLAG lab hello",
                    "summary": "Cached stub until catalog sync is live.",
                }
            ],
            "source": url,
            "note": data.get("error") if isinstance(data, dict) else str(data),
        }
        dest.write_text(json.dumps(stub, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return SyncResult(
            ok=True,
            message=f"stub catalog written to {dest}",
            pulled=True,
            warning=f"catalog GET {status}: {data}",
        )
    return SyncResult(
        ok=True,
        message=f"kept local pack {dest}",
        pulled=False,
        warning=f"catalog GET {status}: {data}",
    )


def push_progress(
    progress_file: Path | None = None, *, user: str | None = None
) -> SyncResult:
    """POST local progress to {base}/api/estudo/mage/progress."""
    path = progress_file or progress_path()
    if not path.exists():
        return SyncResult(ok=False, message=f"no progress file at {path}")
    try:
        progress = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return SyncResult(ok=False, message=f"bad progress json: {exc}")

    auth = load_auth()
    user_key = user or auth.get("user") or os.environ.get("MAGE_USER") or "pedro"
    payload = progress_to_api_payload(progress, user=str(user_key))
    url = f"{api_base()}/api/estudo/mage/progress"
    status, data = _http_json("POST", url, payload)
    if 200 <= status < 300:
        return SyncResult(ok=True, message="progress pushed", pushed=True)
    return SyncResult(
        ok=False,
        message=f"push failed ({status})",
        pushed=False,
        warning=str(data),
    )


def sync_all(*, user: str | None = None) -> SyncResult:
    """Pull systems pack + push progress. Safe offline (writes stubs)."""
    pull = pull_catalog(course="systems")
    push = push_progress(user=user)
    parts = [pull.message, push.message]
    warning = " | ".join(x for x in (pull.warning, push.warning) if x)
    ok = pull.ok or push.ok
    return SyncResult(
        ok=ok,
        message="; ".join(parts),
        pulled=pull.pulled,
        pushed=push.pushed,
        warning=warning,
    )
