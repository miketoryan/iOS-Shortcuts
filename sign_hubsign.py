#!/usr/bin/env python3
"""Sign a vetted, non-sensitive Apple Shortcut plist via Cherri's HubSign API.

Protocol matches open-source Cherri 2.3.0 signing.go:
POST JSON shortcutName / shortcut as XML, User-Agent: cherri/2.3.0.
Does not send any secrets, Apple ID or GitHub authentication data.
"""
import argparse
import json
import plistlib
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ENDPOINT = "https://hubsign.routinehub.services/sign"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="build/verified_unsigned.shortcut")
    p.add_argument("--output", default="build/signed/one-tap-dnd-2h.shortcut")
    p.add_argument("--name", default="一键免打扰（2小时）")
    args = p.parse_args()
    raw = Path(args.input).read_bytes()
    wf = plistlib.loads(raw)
    xml = plistlib.dumps(wf, fmt=plistlib.FMT_XML).decode("utf-8")
    body = json.dumps({"shortcutName": args.name, "shortcut": xml}, ensure_ascii=False).encode("utf-8")
    req = Request(ENDPOINT, data=body, method="POST",
                  headers={"Content-Type": "application/json",
                           "User-Agent": "cherri/2.3.0"})
    try:
        with urlopen(req, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            signed = response.read()
    except HTTPError as exc:
        raise SystemExit(f"HubSign refused the request: HTTP {exc.code}") from None
    except URLError as exc:
        raise SystemExit(f"HubSign network error: {exc.reason}") from None

    if content_type not in ("application/octet-stream", "application/x-plist", "application/x-apple-shortcut"):
        raise SystemExit(f"HubSign responded with unexpected content type: {content_type!r}")
    if len(signed) < 100 or not signed.startswith(b"AEA1"):
        raise SystemExit("HubSign did not return an AEA1 signed archive; nothing will be published")
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(signed)
    print(f"Signed verified shortcut via HubSign: {path}, size={len(signed)}")


if __name__ == "__main__":
    main()
