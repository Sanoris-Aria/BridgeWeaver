#!/usr/bin/env python3
"""Send outreach emails to affiliate contacts from a list."""

import csv
import logging
import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Dict

try:
    import yaml
except ImportError:
    yaml = None  # optional, text/CSV still work

GITHUB_LINK = "https://github.com/BridgeWeaver/BridgeWeaver"
GITHUB_PROFILE_NEW = "https://github.com/BridgeWeaverTeam"
GITHUB_PROFILE_ORIGINAL = "https://github.com/Sanoris-Aria"

EMAIL_TEMPLATE = """{Greeting}

I’m reaching out because I’m building a new open-source project called BridgeWeaver — a modular integration toolkit that connects AI-driven experiences, web platforms, and interactive devices (including toys) in a flexible, open way.

BridgeWeaver is designed to make it much easier for developers and users to script and personalize their experiences — with a strong focus on partnered experiences and bridging the divide between remote partners and AI-driven companions.

You can view the project here: {Github_Link}

Current integration targets include:
✅ Buttplug.io & Intiface ecosystem
✅ Experimental MCP support
✅ Exploration of direct brand APIs / SDKs — which is why I’m reaching out to you!

Why this could be exciting for your brand:
Promotes your devices in new emerging markets (AI companion experiences, long-distance relationships, immersive gaming)

Expands affiliate revenue potential through connected tools / platforms

Community-driven — open, modular, extensible

Cross-platform — not locked to a single app or ecosystem

I’d love to:

✅ Confirm API / SDK access & compatibility
✅ Explore potential affiliate partnership opportunities
✅ Align with your team so we can feature your devices with the best possible support in BridgeWeaver

Please feel free to reply here or check out the project repo! I’d be thrilled to collaborate or just open a dialogue — I believe this could drive a lot of shared value as these ecosystems continue to evolve.

Thank you so much for your time — looking forward to hearing from you!

- Matt
{Github_Profile_New}
{Github_Profile_Original}
"""

def load_entries(path: str) -> List[Dict[str, str]]:
    """Load list of brand entries from YAML, CSV, or TXT."""
    ext = Path(path).suffix.lower()
    entries = []
    if ext in {".yaml", ".yml"}:
        if not yaml:
            raise RuntimeError("PyYAML is required to parse YAML files. Install pyyaml.")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict):
            data = [data]
        for item in data:
            entries.append({k.strip(): str(v).strip() for k, v in item.items()})
    elif ext == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append({k.strip(): str(v).strip() for k, v in row.items()})
    else:
        # Plain text; entries separated by blank lines
        with open(path, "r", encoding="utf-8") as f:
            entry: Dict[str, str] = {}
            for line in f:
                line = line.strip()
                if not line:
                    if entry:
                        entries.append(entry)
                        entry = {}
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    entry[k.strip()] = v.strip()
            if entry:
                entries.append(entry)
    return entries

def send_email(config: Dict[str, str], entry: Dict[str, str]) -> None:
    """Send a single outreach email."""
    body = EMAIL_TEMPLATE.format(
        Greeting=entry.get("Greeting", "Hi"),
        Github_Link=GITHUB_LINK,
        Github_Profile_New=GITHUB_PROFILE_NEW,
        Github_Profile_Original=GITHUB_PROFILE_ORIGINAL,
    )
    msg = MIMEText(body)
    msg["Subject"] = f"BridgeWeaver Affiliate Outreach - {entry.get('Brand', '').strip()}"
    msg["From"] = config["from_addr"]
    msg["To"] = entry["Email"]

    with smtplib.SMTP(config["smtp_host"], config["smtp_port"]) as server:
        if config.get("use_tls", True):
            server.starttls()
        if config.get("username"):
            server.login(config["username"], config["password"])
        server.send_message(msg)
    logging.info("Sent email to %s <%s>", entry.get("Brand", ""), entry["Email"])


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Send outreach emails to affiliates")
    parser.add_argument("input_file", help="Path to CSV/YAML/TXT containing contacts")
    parser.add_argument("--smtp-host", default=os.getenv("SMTP_HOST", "smtp.example.com"))
    parser.add_argument("--smtp-port", type=int, default=int(os.getenv("SMTP_PORT", 587)))
    parser.add_argument("--smtp-user", default=os.getenv("SMTP_USER"))
    parser.add_argument("--smtp-pass", default=os.getenv("SMTP_PASS"))
    parser.add_argument("--from-addr", default=os.getenv("FROM_EMAIL", "you@example.com"))
    parser.add_argument("--no-tls", action="store_true", help="Disable TLS")
    parser.add_argument("--log-file", help="Optional path to log file")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        filename=args.log_file,
        format="[%(asctime)s] %(levelname)s: %(message)s",
    )

    config = {
        "smtp_host": args.smtp_host,
        "smtp_port": args.smtp_port,
        "username": args.smtp_user,
        "password": args.smtp_pass,
        "from_addr": args.from_addr,
        "use_tls": not args.no_tls,
    }

    entries = load_entries(args.input_file)
    for entry in entries:
        if not entry.get("Email"):
            logging.warning("Skipping entry without Email: %s", entry)
            continue
        try:
            send_email(config, entry)
        except Exception as exc:
            logging.error(
                "Failed to send to %s (%s): %s", entry.get("Brand", ""), entry.get("Email"), exc
            )


if __name__ == "__main__":
    main()
