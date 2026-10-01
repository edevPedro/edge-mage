"""GitHub auth stubs for e-mage (device flow → ~/.mage/auth.json).

Env:
  MAGE_API_BASE — API root (default: https://edevs.com or local edevs).
  MAGE_GITHUB_CLIENT_ID — optional OAuth app client id for device flow.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from edge_mage.paths import auth_path, mage_home

DEFAULT_API_BASE = os.environ.get("MAGE_API_BASE", "https://edevs.com").rstrip("/")
GITHUB_DEVICE_CODE_URL = "https://github.com/login/device/code"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"


@dataclass
class DeviceFlowStart:
    """Result of starting (or stubbing) a GitHub device flow."""

    user_code: str
    verification_uri: str
    device_code: str
    interval: int
    expires_in: int
    message: str
    stub: bool = True


def api_base() -> str:
    return os.environ.get("MAGE_API_BASE", DEFAULT_API_BASE).rstrip("/")


def load_auth(path: Path | None = None) -> dict[str, Any]:
    p = path or auth_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_auth(data: dict[str, Any], path: Path | None = None) -> Path:
    p = path or auth_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(data)
    payload["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def start_github_device_flow(*, client_id: str | None = None) -> DeviceFlowStart:
    """
    Start GitHub device authorization.

    Without MAGE_GITHUB_CLIENT_ID (or client_id), returns a stub with
    instructions and writes a placeholder under ~/.mage/auth.json.
    """
    cid = (client_id or os.environ.get("MAGE_GITHUB_CLIENT_ID") or "").strip()
    if not cid:
        stub = DeviceFlowStart(
            user_code="STUB-CODE",
            verification_uri="https://github.com/login/device",
            device_code="",
            interval=5,
            expires_in=900,
            message=(
                "GitHub device flow stub.\n"
                "1. Set MAGE_GITHUB_CLIENT_ID to enable real OAuth device flow.\n"
                "2. Or paste a PAT later into ~/.mage/auth.json as "
                '{"github_token": "ghp_…"}.\n'
                f"3. API base: {api_base()} (MAGE_API_BASE).\n"
                f"4. Auth file: {auth_path()}"
            ),
            stub=True,
        )
        save_auth(
            {
                "provider": "github",
                "status": "stub",
                "verification_uri": stub.verification_uri,
                "user_code": stub.user_code,
                "api_base": api_base(),
                "github_token": None,
            }
        )
        return stub

    body = f"client_id={cid}&scope=read:user".encode()
    req = Request(
        GITHUB_DEVICE_CODE_URL,
        data=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=15) as resp:  # noqa: S310 — intentional GitHub API
            data = json.loads(resp.read().decode())
    except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        save_auth({"provider": "github", "status": "error", "error": str(exc)})
        return DeviceFlowStart(
            user_code="ERROR",
            verification_uri="https://github.com/login/device",
            device_code="",
            interval=5,
            expires_in=0,
            message=f"Device flow failed: {exc}",
            stub=True,
        )

    start = DeviceFlowStart(
        user_code=str(data.get("user_code", "")),
        verification_uri=str(
            data.get("verification_uri") or "https://github.com/login/device"
        ),
        device_code=str(data.get("device_code", "")),
        interval=int(data.get("interval", 5)),
        expires_in=int(data.get("expires_in", 900)),
        message=(
            f"Open {data.get('verification_uri')} and enter code "
            f"{data.get('user_code')}. Waiting is not polled yet — "
            f"save token to {auth_path()} when done."
        ),
        stub=False,
    )
    save_auth(
        {
            "provider": "github",
            "status": "pending",
            "device_code": start.device_code,
            "user_code": start.user_code,
            "verification_uri": start.verification_uri,
            "api_base": api_base(),
            "github_token": None,
        }
    )
    return start


def github_connect_instructions() -> str:
    """Human-readable stub for the launcher 'Conectar GitHub' option."""
    flow = start_github_device_flow()
    home = mage_home()
    return (
        f"{flow.message}\n\n"
        f"Progress home: {home}\n"
        f"Token path (stub): {auth_path()}\n"
        "After connecting, use `:sync` or `mage sync` to push progress."
    )
