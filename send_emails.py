import argparse
import csv
import logging
import os
import smtplib
from email.message import EmailMessage
from typing import List, Dict

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

GITHUB_LINK = "https://github.com/BridgeWeaver/BridgeWeaver"
GITHUB_PROFILE_NEW = "https://github.com/BridgeWeaverTeam"
ORIGINAL_GITHUB_PROFILE = "https://github.com/Sanoris-Aria"

EMAIL_TEMPLATE = """{greeting}

I’m reaching out because I’m building a new open-source project called BridgeWeaver — a modular integration toolkit that connects AI-driven experiences, web platforms, and interactive devices (including toys) in a flexible, open way.

BridgeWeaver is designed to make it much easier for developers and users to script and personalize their experiences — with a strong focus on partnered experiences and bridging the divide between remote partners and AI-driven companions.

You can view the project here: {github_link}

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
{github_profile_new}
{original_github_profile}
"""


def load_entries(path: str) -> List[Dict[str, str]]:
    ext = os.path.splitext(path)[1].lower()
    if ext in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML is required to parse YAML files. Install pyyaml.")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, list):
            raise ValueError("YAML file must contain a list of entries")
        return data
    elif ext == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    else:  # assume custom txt format
        entries = []
        current = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    if current:
                        entries.append(current)
                        current = {}
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    current[key.strip()] = val.strip()
        if current:
            entries.append(current)
        return entries


def send_email(entry: Dict[str, str], smtp_config: Dict[str, str], dry_run: bool = False) -> None:
    msg = EmailMessage()
    msg["Subject"] = "BridgeWeaver Integration Inquiry"
    msg["From"] = smtp_config["from_email"]
    msg["To"] = entry["Email"]
    body = EMAIL_TEMPLATE.format(
        greeting=entry.get("Greeting", "Hi there"),
        github_link=GITHUB_LINK,
        github_profile_new=GITHUB_PROFILE_NEW,
        original_github_profile=ORIGINAL_GITHUB_PROFILE,
    )
    msg.set_content(body)

    if dry_run:
        logging.info("DRY RUN: Would send to %s", entry["Email"])
        logging.debug("Email body:\n%s", body)
        return

    with smtplib.SMTP(smtp_config["host"], smtp_config.get("port", 587)) as server:
        server.starttls()
        server.login(smtp_config["user"], smtp_config["password"])
        server.send_message(msg)
    logging.info("Sent email to %s", entry["Email"])


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Send outreach emails to affiliate contacts")
    ap.add_argument("input", help="Path to contacts file (.yaml, .csv, or .txt)")
    ap.add_argument("--log", default=None, help="Optional log file path")
    ap.add_argument("--dry-run", action="store_true", help="Log emails instead of sending")
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(level=logging.INFO, filename=args.log, format="%(levelname)s: %(message)s")

    smtp_config = {
        "host": os.getenv("SMTP_HOST", "smtp.example.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": os.getenv("SMTP_USER", "user@example.com"),
        "password": os.getenv("SMTP_PASSWORD", "password"),
        "from_email": os.getenv("FROM_EMAIL", "noreply@example.com"),
    }

    entries = load_entries(args.input)
    for entry in entries:
        required = ["Brand", "Email", "Greeting"]
        if not all(k in entry for k in required):
            logging.warning("Skipping entry missing required fields: %s", entry)
            continue
        send_email(entry, smtp_config, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
