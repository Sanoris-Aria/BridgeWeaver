import argparse
import smtplib
from email.message import EmailMessage
import logging

TEMPLATE = """{greeting}

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
{new_profile}
{original_profile}
"""


def parse_contacts(path: str):
    contacts = []
    with open(path, "r", encoding="utf-8") as f:
        block = []
        for line in f:
            line = line.strip()
            if not line:
                if block:
                    contacts.append(parse_block(block))
                    block = []
            else:
                block.append(line)
        if block:
            contacts.append(parse_block(block))
    return contacts


def parse_block(lines):
    data = {}
    for line in lines:
        if line.startswith("Brand:"):
            data["brand"] = line.split(":", 1)[1].strip()
        elif line.startswith("Email:"):
            data["email"] = line.split(":", 1)[1].strip()
        elif line.startswith("Greeting:"):
            data["greeting"] = line.split(":", 1)[1].strip()
        elif line.startswith("Source:"):
            data["source"] = line.split(":", 1)[1].strip()
    return data


def send_email(entry, smtp_conf, github_link, new_profile, original_profile, logger):
    msg = EmailMessage()
    msg["Subject"] = "BridgeWeaver Affiliate Inquiry"
    msg["From"] = smtp_conf["from_addr"]
    msg["To"] = entry["email"]

    body = TEMPLATE.format(
        greeting=entry.get("greeting", "Hi"),
        github_link=github_link,
        new_profile=new_profile,
        original_profile=original_profile,
    )
    msg.set_content(body)

    with smtplib.SMTP(smtp_conf["host"], smtp_conf.get("port", 25)) as server:
        if smtp_conf.get("starttls"):
            server.starttls()
        if smtp_conf.get("user") and smtp_conf.get("password"):
            server.login(smtp_conf["user"], smtp_conf["password"])
        server.send_message(msg)
    logger.info("Sent email to %s <%s>", entry.get("brand"), entry.get("email"))


def main():
    parser = argparse.ArgumentParser(description="Send outreach emails to affiliates")
    parser.add_argument("input", help="Path to contacts list (txt)")
    parser.add_argument("--smtp-host", default="smtp.example.com")
    parser.add_argument("--smtp-port", type=int, default=587)
    parser.add_argument("--smtp-user", default="user@example.com")
    parser.add_argument("--smtp-password", default="password")
    parser.add_argument("--from-addr", default="user@example.com")
    parser.add_argument("--github-link", default="https://github.com/BridgeWeaver/BridgeWeaver")
    parser.add_argument("--new-profile", default="https://github.com/BridgeWeaverTeam")
    parser.add_argument("--original-profile", default="https://github.com/Sanoris-Aria")
    parser.add_argument("--log-file", default=None)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, filename=args.log_file, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("emailer")
    contacts = parse_contacts(args.input)

    smtp_conf = {
        "host": args.smtp_host,
        "port": args.smtp_port,
        "user": args.smtp_user,
        "password": args.smtp_password,
        "from_addr": args.from_addr,
        "starttls": True,
    }

    for entry in contacts:
        if "email" not in entry:
            logger.warning("Skipping entry without email: %s", entry)
            continue
        send_email(entry, smtp_conf, args.github_link, args.new_profile, args.original_profile, logger)


if __name__ == "__main__":
    main()
