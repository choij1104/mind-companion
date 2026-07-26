# Mind Companion

A simple, private memory aid for older adults.

Ask a question out loud and get a spoken answer. Track medicine, keep contacts one tap
from a phone call, store emergency information, and write down where things are.
Everything stays on the device — no account, no server, no tracking.

**Live app:** https://choij1104.github.io/mind-companion/

---

## What it does

| Screen | Purpose |
|---|---|
| **Home** | Large clock and date, one big microphone button, today's medicine at a glance |
| **Medicine** | A checklist of daily medicine; tap the large square when taken |
| **Contacts** | Name, role, and a green button that dials directly |
| **Notes** | "Where did I put the passport?" — written by voice or by typing, searchable by voice |
| **Help** | Call 911, call family directly, and show conditions, allergies, and blood type to paramedics |
| **Settings** | Text size, language, backup and restore, notices |

Ask by voice and the app answers from what is stored:

- "What day is it today?"
- "Did I take my medicine?"
- "Who is my doctor?"
- "Where is my passport?"

## Conversation

Out of the box the app answers from fixed rules — the day, medicine, contacts, notes, and
greetings. It works offline and sends nothing anywhere.

Connect it to a small free relay and it holds an actual conversation instead: the person can
say anything and get a natural spoken reply, informed by what is saved in the app. Setup takes
about ten minutes and is described in **[SETUP-CONVERSATION.md](SETUP-CONVERSATION.md)**.

The relay exists so the API key stays off the public web page. Conversation is optional and
off until an address is entered in Settings.

Whichever mode is used, the app never diagnoses, never advises on medicine, and directs
health questions to a doctor or pharmacist.

## Designed for older users

- Base text 18 px, enlargeable to 1.45× from Settings; the setting is remembered
- All touch targets at least 56 px; the microphone button is 132 px, the 911 button 96 px
- Five fixed tabs at the bottom, within thumb reach
- High-contrast palette; visible keyboard focus; reduced motion respected
- Every deletion asks for confirmation
- Spoken output is slowed to 0.88× for easier listening

## Privacy

No accounts, no analytics, no network requests for user data. All information is kept in the
browser's local storage on the device. See [PRIVACY.md](PRIVACY.md).

Because storage is local, **clearing browser data or replacing the phone will erase everything.**
Use **Settings → Save a backup file** and keep the file somewhere safe.

## Requirements

- **Voice input** needs Chrome or Safari (Web Speech API). Firefox does not support it.
  On iPhone, voice input works in Safari.
- Without voice support the app still works fully — use **Type a question instead**.
- Works offline after the first visit (service worker caches the app shell).

## Install on a phone

1. Open the app link in Chrome (Android) or Safari (iPhone)
2. Android: menu → **Add to Home screen**. iPhone: share button → **Add to Home Screen**
3. It then opens full-screen like an app

## Setting it up for someone

1. Open **Help → Edit my information** and fill in name, address, conditions, allergies, blood type
2. Add family under **Contacts** with the role *Family* — they appear as large call buttons on the Help screen
3. Add the doctor and pharmacy so "Who is my doctor?" can be answered
4. Add daily medicine under **Medicine**
5. Set the text size, then **Settings → Save a backup file**

## Deploying

Static site, no build step.

```
git clone https://github.com/choij1104/mind-companion.git
cd mind-companion
# copy the files in, then
git add .
git commit -m "Mind Companion v1.3"
git push origin main
```

Then in the repository: **Settings → Pages → Source: main / (root) → Save**.

Files:

```
index.html                 the whole app
manifest.json              PWA metadata
sw.js                      offline cache
worker.js                  optional relay — NOT uploaded to GitHub Pages
icon-192.png               app icons
icon-512.png
icon-maskable-512.png
apple-touch-icon.png
favicon-32.png
.nojekyll                  serve files as-is
README.md
SETUP-CONVERSATION.md
PRIVACY.md
LICENSE
```

`worker.js` is not part of the website. It is pasted into a Cloudflare Worker; see
SETUP-CONVERSATION.md. Keeping it in the repository is fine — it holds no key.

When releasing an update, bump `CACHE` in `sw.js` (for example `mind-companion-v1.3`)
so devices pick up the new version instead of serving the old cache.

## Important notice

Mind Companion is a personal memory aid. It is **not a medical device** and does not give
medical advice. It does not sound alarms and must not be relied on as a medication reminder.
Always follow the instructions of a doctor or pharmacist. In an emergency, call 911 or the
local emergency number.

## License

MIT — see [LICENSE](LICENSE).

© 2026 Jae Hyek Choi
