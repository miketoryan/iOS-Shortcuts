#!/usr/bin/env python3
"""Try legacy RoutineHub HubSign's publicly documented JSON signing endpoint.

This is an optional third-party signer. It receives only the unsigned shortcut
definition and no Apple ID or GitHub credentials. Never bypass authentication:
if the service reports that a key or membership is required, stop and fail.
"""
import argparse
import json
import plistlib
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ENDPOINT = "https://hubsign.routinehub.services/sign"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="build/unsigned/one-tap-dnd-2h.shortcut")
    parser.add_argument("--output", default="build/signed/one-tap-dnd-2h.shortcut")
    parser.add_argument("--name", default="一键免打扰（2小时）")
    args = parser.parse_args()
    raw = Path(args.input).read_bytes()
    workflow = plistlib.loads(raw)
    xml = plistlib.dumps(workflow, fmt=plistlib.FMT_XML).decode("utf-8")
    payload = json.dumps({
        "shortcutName": args.name,
        "shortcut": xml,
    }, ensure_ascii=False).encode("utf-8")
    req = Request(
        ENDPOINT,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/octet-stream",
            "User-Agent": "ios-shortcuts-workflow/1.0",
            "Origin": "https://routinehub.co",
            "Referer": "https://routinehub.co/",
        },
    )
    try:
        with urlopen(req, timeout=30) as response:
            signed = response.read()
    except HTTPError as exc:
        # Do not retry on authentication, membership, access or policy responses.
        raise SystemExit(f"HubSign refused signing: HTTP {exc.code}") from None
    except URLError as exc:
        raise SystemExit(f"HubSign unavailable: {exc.reason}") from None

    if not signed.startswith(b"AEA1"):
        raise SystemExit("HubSign returned non-AEA1 data: refusing to publish")
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(signed)
    print(f"HubSign AEA1 archive received: {len(signed)} bytes")


if __name__ == "__main__":
    main()
