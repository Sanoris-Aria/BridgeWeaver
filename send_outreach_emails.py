import argparse
import csv
import logging
import io
import os
import smtplib
import sys
from email.message import EmailMessage
from typing import List, Dict

try:
    import yaml
except ImportError:  # pragma: no cover - handle missing yaml gracefully
    yaml = None

GITHUB_LINK = "https://github.com/Sanoris-Aria/BridgeWeaver"
GITHUB_PROFILE_NEW = "https://github.com/Sanoris-Aria"
GITHUB_PROFILE_ORIGINAL = "https://github.com/Sanoris"

EMAIL_TEMPLATE = """{greeting},

I’m reaching out because I’m building a new open-source project called **BridgeWeaver** — a modular integration toolkit that connects AI-driven experiences, web platforms, and interactive devices (including toys) in a flexible, open way.

**BridgeWeaver** is designed to make it much easier for developers and users to script and personalize their experiences — with a strong focus on partnered experiences and bridging the divide between remote partners and AI-driven companions.

You can view the project here: {github_link}

---

**Current integration targets include:**
✅ Buttplug.io & Intiface ecosystem  
✅ Experimental MCP support  
✅ Exploration of direct brand APIs / SDKs — which is why I’m reaching out to you!  

---

**Why this could be exciting for your brand:**  
- Promotes your devices in new emerging markets (AI companion experiences, long-distance relationships, immersive gaming)  
- Expands affiliate revenue potential through connected tools / platforms  
- Community-driven — open, modular, extensible  
- Cross-platform — not locked to a single app or ecosystem  

---

**I’d love to:**  
✅ Confirm API / SDK access & compatibility  
✅ Explore potential affiliate partnership opportunities  
✅ Align with your team so we can feature your devices with the best possible support in BridgeWeaver  

---

Please feel free to reply here or check out the project repo! I’d be thrilled to collaborate or just open a dialogue — I believe this could drive a lot of shared value as these ecosystems continue to evolve.

Thank you so much for your time — looking forward to hearing from you!

Best regards,  
Matt  
{github_profile_new}  
{github_profile_original}
"""


DEFAULT_SMTP_HOST = "smtp.example.com"
DEFAULT_SMTP_PORT = 587
DEFAULT_SMTP_USER = "Matt Hendricks"
DEFAULT_SMTP_PASSWORD = "password"
DEFAULT_FROM_EMAIL = "you@example.com"
DEFAULT_SUBJECT = "BridgeWeaver Integration Inquiry"


def load_contacts(path: str) -> List[Dict[str, str]]:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("PyYAML is required to load YAML files")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, list):
            raise ValueError("YAML file must contain a list of mappings")
        return data
    elif ext == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    else:
        raise ValueError("Unsupported file type: %s" % ext)


def create_message(entry: Dict[str, str]) -> str:
    greeting = entry.get("Greeting") or f"Hi {entry.get('Brand', '').strip()} Team"
    return EMAIL_TEMPLATE.format(
        greeting=greeting,
        github_link=GITHUB_LINK,
        github_profile_new=GITHUB_PROFILE_NEW,
        github_profile_original=GITHUB_PROFILE_ORIGINAL,
    )


def send_email(smtp: smtplib.SMTP, sender: str, recipient: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    smtp.send_message(msg)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send outreach emails to contacts")
    parser.add_argument("input_file", help="Path to contacts file (yaml or csv)")
    parser.add_argument("--smtp-host", default=DEFAULT_SMTP_HOST)
    parser.add_argument("--smtp-port", type=int, default=DEFAULT_SMTP_PORT)
    parser.add_argument("--smtp-user", default=DEFAULT_SMTP_USER)
    parser.add_argument("--smtp-password", default=DEFAULT_SMTP_PASSWORD)
    parser.add_argument("--from-email", default=DEFAULT_FROM_EMAIL)
    parser.add_argument("--subject", default=DEFAULT_SUBJECT)
    parser.add_argument("--dry-run", action="store_true", help="Print emails without sending")
    parser.add_argument("--log-file", default=None, help="Optional log file path")
    args = parser.parse_args()

    # Explicitly set UTF-8 encoding for the log file using a FileHandler
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    contacts = load_contacts(args.input_file)

    if args.dry_run:
        smtp = None
    else:
        smtp = smtplib.SMTP(args.smtp_host, args.smtp_port)
        smtp.starttls()
        smtp.login(args.smtp_user, args.smtp_password)

    for entry in contacts:
        to_email = entry.get("Email")
        if not to_email:
            logging.warning("Skipping entry without email: %s", entry)
            continue
        body = create_message(entry)
        # Updated the dry-run logic to log the full email message to the log file
        if args.dry_run:
            logging.info("[DRY RUN] Would send email to %s (%s) with message:\n%s", entry.get("Brand"), to_email, body)
            continue
        send_email(smtp, args.from_email, to_email, args.subject, body)
        logging.info("Sent email to %s (%s)", entry.get("Brand"), to_email)

    if smtp is not None:
        smtp.quit()


# Ensure logging uses UTF-8 encoding to avoid character encoding issues
# Set UTF-8 encoding for stdout and stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

if __name__ == "__main__":
    main()
