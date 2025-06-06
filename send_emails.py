import csv
import os
import smtplib
from email.message import EmailMessage

try:
    import yaml
except ImportError:  # pragma: no cover - yaml optional
    yaml = None

TEMPLATE = """{greeting}

I'm reaching out because I'm building a new open-source project called BridgeWeaver — a modular integration toolkit that connects AI-driven experiences, web platforms, and interactive devices (including toys) in a flexible, open way.

BridgeWeaver is designed to make it much easier for developers and users to script and personalize their experiences — with a strong focus on partnered experiences and bridging the divide between remote partners and AI-driven companions.

You can view the project here: {github_link}

Current integration targets include:
✅ Buttplug.io & Intiface ecosystem
✅ Experimental MCP support
✅ Exploration of direct brand APIs / SDKs — which is why I'm reaching out to you!

Why this could be exciting for your brand:
Promotes your devices in new emerging markets (AI companion experiences, long-distance relationships, immersive gaming)

Expands affiliate revenue potential through connected tools / platforms

Community-driven — open, modular, extensible

Cross-platform — not locked to a single app or ecosystem

I'd love to:

✅ Confirm API / SDK access & compatibility
✅ Explore potential affiliate partnership opportunities
✅ Align with your team so we can feature your devices with the best possible support in BridgeWeaver

Please feel free to reply here or check out the project repo! I'd be thrilled to collaborate or just open a dialogue — I believe this could drive a lot of shared value as these ecosystems continue to evolve.

Thank you so much for your time — looking forward to hearing from you!

- Matt
{github_profile_new}
{github_profile_original}
"""

DEFAULTS = {
    "github_link": "https://github.com/BridgeWeaver/BridgeWeaver",
    "github_profile_new": "https://github.com/BridgeWeaverTeam",
    "github_profile_original": "https://github.com/Sanoris-Aria",
}


def load_contacts(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in {".yml", ".yaml"}:
        if not yaml:
            raise RuntimeError("PyYAML required for YAML input")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return [
            {
                "brand": entry.get("Brand"),
                "email": entry.get("Email"),
                "greeting": entry.get("Greeting"),
                "source": entry.get("Source"),
            }
            for entry in data
        ]
    elif ext == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [
                {
                    "brand": row.get("Brand"),
                    "email": row.get("Email"),
                    "greeting": row.get("Greeting"),
                    "source": row.get("Source"),
                }
                for row in reader
            ]
    elif ext == ".txt":
        contacts = []
        with open(path, encoding="utf-8") as f:
            block = {}
            for line in f:
                line = line.strip()
                if not line:
                    if block:
                        contacts.append(block)
                        block = {}
                    continue
                if line.startswith("Brand:"):
                    block["brand"] = line.split(":", 1)[1].strip()
                elif line.startswith("Email:"):
                    block["email"] = line.split(":", 1)[1].strip()
                elif line.startswith("Greeting:"):
                    block["greeting"] = line.split(":", 1)[1].strip()
                elif line.startswith("Source:"):
                    block["source"] = line.split(":", 1)[1].strip()
            if block:
                contacts.append(block)
        return contacts
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def send_email(contact, smtp_config):
    msg = EmailMessage()
    msg["From"] = smtp_config.get("from_addr")
    msg["To"] = contact["email"]
    msg["Subject"] = f"BridgeWeaver Partnership Inquiry — {contact['brand']}"
    body = TEMPLATE.format(
        greeting=contact["greeting"],
        github_link=DEFAULTS["github_link"],
        github_profile_new=DEFAULTS["github_profile_new"],
        github_profile_original=DEFAULTS["github_profile_original"],
    )
    msg.set_content(body)

    with smtplib.SMTP(smtp_config.get("host"), smtp_config.get("port")) as smtp:
        if smtp_config.get("starttls", True):
            smtp.starttls()
        if smtp_config.get("username"):
            smtp.login(smtp_config.get("username"), smtp_config.get("password"))
        smtp.send_message(msg)
    print(f"Sent email to {contact['brand']} <{contact['email']}>")


def main(path):
    smtp_config = {
        "host": "smtp.example.com",
        "port": 587,
        "username": "user@example.com",
        "password": "replace-with-password",
        "from_addr": "user@example.com",
        "starttls": True,
    }

    contacts = load_contacts(path)
    for contact in contacts:
        send_email(contact, smtp_config)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Send outreach emails to contacts")
    parser.add_argument("path", help="Path to contacts file (.txt, .yaml, .csv)")
    args = parser.parse_args()
    main(args.path)
