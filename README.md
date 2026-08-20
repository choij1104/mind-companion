# Mind Companion

A simple, private memory aid and daily mind check-in for older adults.

Ask a question out loud and get a spoken answer. Track medicine, keep contacts one tap
from a phone call, store emergency information, write down where things are, and record
how the day felt. Everything stays on the device — no account, no server, no tracking.

**Live app:** https://choij1104.github.io/mind-companion/

---

## What it does

| Screen | Purpose |
|---|---|
| **Home** | Large clock, date, and time-of-day line, one big microphone button, today's medicine at a glance |
| **Medicine** | A checklist of daily medicine; tap the large square when taken |
| **Contacts** | Name, role, and a green button that dials directly |
| **Notes** | "Where did I put the passport?" — written by voice or by typing, searchable by voice |
| **Mind** | Daily mood, a two-question check-in, a summary page to bring to counseling, and the counselor's number |
| **Help** | Call 911, call family directly, and show conditions, allergies, and blood type to paramedics |
| **Settings** | Text size, language, conversation, backup and restore, caregiver tools, notices |

Ask by voice and the app answers from what is stored:

- "What day is it today?"
- "Did I take my medicine?"
- "Who is my doctor?"
- "Where is my passport?"
- "Where do I live?"

## Languages

English, 한국어, Español, 日本語 — chosen in Settings. English is the default. Every screen,
question, and notice is translated; the spoken voice follows the chosen language.

## Conversation

Out of the box the app answers from fixed rules — the day, medicine, contacts, notes, identity,
and greetings. It works offline and sends nothing anywhere.

Connect it to a small free relay and it holds an actual conversation instead: the person can
say anything and get a natural spoken reply, informed by what is saved in the app. Setup takes
about ten minutes and is described in **[SETUP-CONVERSATION.md](SETUP-CONVERSATION.md)**.

The relay exists so the API key stays off the public web page. Conversation is optional and
off until an address is entered in Settings. If the relay is unreachable, the app falls back to
its offline answers without an error.

Whichever mode is used, the app never diagnoses, never advises on medicine, and directs
health questions to a doctor or pharmacist.

## For caregivers and program staff

Under **Settings → Caregiver · program staff**:

- **Simple Mode** reduces the interface for someone with more advanced memory difficulty.
- **4-week report** saves a printable page: medicine marks, daily mood, mind check answers,
  and points worth discussing.
- **Data file (CSV)** saves the same records as a spreadsheet.

Marks in the app are made by the person using it. They show engagement with the app, not
verified intake, and the report says so.

## Designed for older users

- Base text 18 px, enlargeable to 1.45× from Settings; the setting is remembered
- Primary buttons at least 64 px tall; the microphone button is 132 px, the 911 button 96 px
- Six fixed tabs at the bottom, within thumb reach
- High-contrast palette; visible keyboard focus; reduced motion respected
- Every deletion asks for confirmation
- Spoken output is slowed for easier listening

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
5. Add the counselor under **Mind** if the person is in a counseling program
6. Set the language and text size, then **Settings → Save a backup file**

## Deploying

Static site, no build step.

```
git clone https://github.com/choij1104/mind-companion.git
cd mind-companion
# copy the files in, then
git add .
git commit -m "Mind Companion v1.5"
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
CHANGELOG.md
SETUP-CONVERSATION.md
PRIVACY.md
LICENSE
```

`worker.js` is not part of the website. It is pasted into a Cloudflare Worker; see
SETUP-CONVERSATION.md. Keeping it in the repository is fine — it holds no key.

**Every release must bump `CACHE` in `sw.js`** (for example `mind-companion-v1.5`), or devices
keep serving the old cached files. `APP_VERSION` in `index.html`, the version in the page
footer, and `CACHE` in `sw.js` must all name the same version.

## Important notice

Mind Companion is a personal memory aid. It is **not a medical device** and does not give
medical advice. It does not sound alarms and must not be relied on as a medication reminder.
The two-question mind check is a simple self-reflection, not a medical test, a screening
result, or a diagnosis. Always follow the instructions of a doctor or pharmacist. In an
emergency, call 911 or the local emergency number.

## License

Proprietary. Free to use as deployed by the copyright holder, for personal, non-commercial
purposes. Copying, redistributing, modifying, translating, or commercial use requires prior
written permission. See [LICENSE](LICENSE).

© 2026 Jae Hyek Choi / HAKOYA LLC. All rights reserved.
