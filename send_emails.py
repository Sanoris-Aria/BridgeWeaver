import argparse
import csv
import logging
import smtplib
from email.message import EmailMessage
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# Placeholder SMTP configuration - replace with real credentials
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "user@example.com"
SMTP_PASS = "password"

GITHUB_LINK = "https://github.com/BridgeWeaver/BridgeWeaver"
GITHUB_PROFILE_NEW = "https://github.com/BridgeWeaverTeam"
GITHUB_PROFILE_ORIG = "https://github.com/Sanoris-Aria"

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
{github_profile_orig}
"""


def load_entries(path: Path):
    ext = path.suffix.lower()
    if ext in {".yaml", ".yml"}:
        if not yaml:
            raise RuntimeError("PyYAML is required to read YAML files")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, list):
            return data
        raise ValueError("YAML root must be a list of entries")
    elif ext == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    elif ext == ".txt":
        entries = []
        current = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    if current:
                        entries.append(current)
                        current = {}
                    continue
                if ":" in line:
                    key, val = map(str.strip, line.split(":", 1))
                    current[key] = val
            if current:
                entries.append(current)
        return entries
    else:
        raise ValueError(f"Unsupported input extension: {ext}")


def build_email(entry: dict) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = entry.get("Email")
    msg["Subject"] = f"BridgeWeaver Affiliate Outreach - {entry.get('Brand', '')}".strip()
    body = EMAIL_TEMPLATE.format(
        greeting=entry.get("Greeting", "Hi there"),
        github_link=GITHUB_LINK,
        github_profile_new=GITHUB_PROFILE_NEW,
        github_profile_orig=GITHUB_PROFILE_ORIG,
    )
    msg.set_content(body)
    return msg


def send_emails(entries):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        for entry in entries:
            msg = build_email(entry)
            smtp.send_message(msg)
            logging.info("Sent email to %s (%s)", entry.get("Brand"), entry.get("Email"))
            print(f"Sent email to {entry.get('Brand')} <{entry.get('Email')}>")


def main():
    parser = argparse.ArgumentParser(description="Send BridgeWeaver outreach emails")
    parser.add_argument("input_file", help="Path to contacts (.txt, .yaml, .csv)")
    parser.add_argument("--log", dest="logfile", help="Optional log file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, filename=args.logfile, format="%(asctime)s - %(message)s")

    entries = load_entries(Path(args.input_file))
    send_emails(entries)


if __name__ == "__main__":
    main()
