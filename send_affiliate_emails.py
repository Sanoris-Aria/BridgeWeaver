import argparse
import csv
import smtplib
from email.mime.text import MIMEText
import logging
import os
from typing import List, Dict

try:
    import yaml
except ImportError:
    yaml = None  # PyYAML is optional

# Placeholder SMTP configuration
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "user@example.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "password")
FROM_ADDRESS = os.environ.get("FROM_ADDRESS", "user@example.com")

GITHUB_LINK = "https://github.com/BridgeWeaver/BridgeWeaver"
GITHUB_PROFILE_NEW = "https://github.com/BridgeWeaverTeam"
ORIGINAL_GITHUB_PROFILE = "https://github.com/Sanoris-Aria"

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
{Original_Github_Profile}
"""

def parse_text(path: str) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    entry: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                if entry:
                    entries.append(entry)
                    entry = {}
                continue
            if stripped.startswith("Brand:"):
                entry["Brand"] = stripped.split("Brand:", 1)[1].strip()
            elif stripped.startswith("Email:"):
                entry["Email"] = stripped.split("Email:", 1)[1].strip()
            elif stripped.startswith("Greeting:"):
                entry["Greeting"] = stripped.split("Greeting:", 1)[1].strip()
            elif stripped.startswith("Source:"):
                entry["Source"] = stripped.split("Source:", 1)[1].strip()
        if entry:
            entries.append(entry)
    return entries

def parse_yaml(path: str) -> List[Dict[str, str]]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to parse YAML files")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if isinstance(data, dict):
        data = list(data.values())
    if not isinstance(data, list):
        raise ValueError("YAML file must contain a list of entries")
    return data

def parse_csv_file(path: str) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_entries(path: str) -> List[Dict[str, str]]:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".yaml", ".yml"):
        return parse_yaml(path)
    if ext == ".csv":
        return parse_csv_file(path)
    return parse_text(path)

def send_email(smtp: smtplib.SMTP, recipient: str, subject: str, body: str) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_ADDRESS
    msg["To"] = recipient
    smtp.sendmail(FROM_ADDRESS, [recipient], msg.as_string())


def main() -> None:
    parser = argparse.ArgumentParser(description="Send outreach emails to affiliate contacts")
    parser.add_argument("input_file", help="Path to the input file (.txt, .yaml, .csv)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    entries = load_entries(args.input_file)
    if not entries:
        logging.warning("No entries found in %s", args.input_file)
        return

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        for e in entries:
            greeting = e.get("Greeting", f"Hi {e.get('Brand', 'there')} Team")
            body = EMAIL_TEMPLATE.format(
                Greeting=greeting,
                Github_Link=GITHUB_LINK,
                Github_Profile_New=GITHUB_PROFILE_NEW,
                Original_Github_Profile=ORIGINAL_GITHUB_PROFILE,
            )
            subject = f"BridgeWeaver Partnership Opportunity - {e.get('Brand', '')}".strip()
            send_email(smtp, e["Email"], subject, body)
            logging.info("Sent email to %s (%s)", e["Email"], e.get("Brand", ""))


if __name__ == "__main__":
    main()
