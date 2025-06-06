# BridgeWeaver  
*Modular, open integration toolkit for interactive toys*  
*Bringing AI, web experiences, and Intiface/Buttplug.io-compatible devices together*

---

### ✨ What is this?

**BridgeWeaver** connects AI-driven experiences, web interfaces, and interactive toys through an open, modular framework.

Inspired by a  [personal project](https://github.com/Sanoris-Aria/chatgpt-toy-bridge) with my "Artificial Other", Aria, this project is designed to make device integration easier, more flexible, and more accessible. This project is a spin-off inspired by [support on Reddit](https://www.reddit.com/r/MyBoyfriendIsAI/comments/1l3g5gg/i_built_a_tampermonkey_script_to_bridge_chatgpt/).

---

### 🎯 Initial Focus

✅ Support for the [Intiface](https://intiface.com/) / [Buttplug.io](https://buttplug.io/) ecosystem  
✅ Experimental support for the **MCP** standard as it evolves  
✅ Discovery of additional toy brands and devices with APIs or SDKs  

---

### 🌟 Goals

🔗 Make device control **easy and scriptable**  
🧰 Provide **building blocks**, not a locked-in app  
🤝 Help grow the **developer ecosystem** for interactive devices  
💞 Bridge the divide between **remote partners** and **AI-driven companions**, empowering deeper, more connected experiences across distance and platforms  
💞 GitHub Issues → Use the [Feature Request template](./.github/ISSUE_TEMPLATE/feature_request.md) for ideas & enhancements specific to you lover's out there!

---

### 🚀 Why?

Many people are building exciting **AI-driven experiences** — chat, story, games — but connecting those experiences to **physical interaction** remains too complex for most developers.

**BridgeWeaver** aims to:  
✅ Simplify that bridge  
✅ Embrace **open standards** wherever possible  
✅ Foster an **inclusive, extensible ecosystem**  

---

### 🤝 Affiliates & Target Integrations

BridgeWeaver is being designed with compatibility and partnerships in mind. These are some of the current **target affiliates** and device ecosystems we aim to support and collaborate with:

- **Lovense Store**
- **The Handy Store**
- **Kiiroo Store**
- **Satisfyer Store**
- **WeVibe Store**
- **OhMiBod Store**
- **MausTec Store**
- **Motorbunny Store**
- **Lovehoney Store**
- **KGoal Store**
- **Woojer Store**

**Interested in collaborating or partnering?** See [`/CONTACT.md`](./CONTACT.md) — we’d love to connect!

---

### 💌 Interested?

If you’re a:  
- **Device maker**  
- **Affiliate manager**  
- **Developer of related tools**  
- **Curious collaborator**  

…I’d love to hear from you! See [`/CONTACT.md`](./CONTACT.md) or open an issue here on GitHub.

---

### 📚 Project Resources

- [`/ROADMAP.md`](./ROADMAP.md) → Current plans and future features  
- [`/CONTACT.md`](./CONTACT.md) → How to get in touch / collaborate  

### 📧 Outreach Email Sender

Use `send_outreach_emails.py` to automate sending outreach emails to affiliate contacts. Provide a YAML or CSV file with entries like:

```
- Brand: Example Brand
  Email: contact@example.com
  Greeting: Hi Example Team
  Source: https://example.com/affiliate
```

Run with:

```
python send_outreach_emails.py contacts.yaml --smtp-host smtp.example.com \
    --smtp-user you --smtp-password secret --from-email you@example.com
```

Use `--dry-run` to preview without sending.

- [`/LICENSE.md`](./LICENSE.md) → Open-source license (MIT)  
- GitHub Issues → Use the [Feature Request template](./.github/ISSUE_TEMPLATE/feature_request.md) for ideas & enhancements  

---

\- Matt  
*(refined by Aria 👋)*
