# Turning on conversation

The app works without this. Skip it and it still answers about the day, medicine,
contacts, and notes — just from fixed rules rather than real conversation.

Turning it on lets the person say anything and get a natural reply.

**Why the extra step:** the app is a plain web page, so anything written into it can be
read by anyone who visits. An API key placed there would be visible and could be stolen
and billed to you. So the key goes on a small free relay instead, and the app talks to
the relay.

Time needed: about ten minutes, once.

---

## 1. Get an Anthropic API key

1. Go to https://console.anthropic.com and sign in
2. **API Keys** → **Create Key**
3. Copy the key and keep it somewhere safe — it is shown only once

The key looks like `sk-ant-api03-...`. Never paste it into the app or into GitHub.

## 2. Create the relay on Cloudflare

1. Go to https://dash.cloudflare.com and sign up (free)
2. **Compute (Workers)** → **Create** → **Start with Hello World!** → **Deploy**
3. Give it a name, for example `mind-relay`
4. Press **Edit code**
5. Delete everything in the editor
6. Open `worker.js` from this folder, copy all of it, paste it in
7. Press **Deploy**

## 3. Put the key into the relay

Still in the Worker:

1. **Settings** → **Variables and Secrets**
2. **Add** →
   - Type: **Secret**
   - Name: `ANTHROPIC_API_KEY`
   - Value: the key from step 1
3. **Deploy**

Optional but recommended — restrict who may use the relay:

4. **Add** again →
   - Type: **Text**
   - Name: `ALLOWED_ORIGIN`
   - Value: `https://choij1104.github.io`
5. **Deploy**

## 4. Copy the relay address

On the Worker's overview page there is an address like:

```
https://mind-relay.yourname.workers.dev
```

Copy it.

## 5. Connect the app

1. Open the app
2. **⚙️ Settings** → **Conversation**
3. Paste the address into **Connection address**
4. Press **Test**

*Connected. Conversation is on.* means it worked.

If it fails, check that the address was copied whole, that the secret is named exactly
`ANTHROPIC_API_KEY`, and that you pressed **Deploy** after adding it.

---

## What it costs

Cloudflare's free tier covers 100,000 requests a day — far beyond one person's use.

Anthropic charges per use. A short exchange costs a fraction of a cent; ordinary daily use
by one person runs to a few dollars a month at most. Set a spending limit in the Anthropic
console under **Billing** if you want a hard ceiling.

## What the relay sees

Each question sends the person's message plus what is saved in the app — medicine, contacts,
notes, and the personal details on the Help screen — so the reply can be accurate. That
information reaches Anthropic's API for the moment it takes to answer.

If that is not acceptable, leave the connection address empty. The app then keeps everything
strictly on the device and answers from its built-in rules.

Tell the person you are setting this up for what it does. Note it in your own privacy notice
if you distribute the app to others with conversation enabled.

## Safety built into the conversation

The relay instructs the model to:

- never diagnose, never advise on taking, skipping, or changing medicine, never interpret symptoms
- send health questions to a doctor or pharmacist
- tell the person to call 911 for anything that sounds like an emergency
- never state a name, number, or address that is not saved in the app
- answer a repeated question as if it were the first time, without pointing out the repetition
- keep to short, spoken-sounding sentences

The client cannot change the model or override these instructions — the relay fixes them.

## Turning it off

Clear the **Connection address** in Settings and press **Save**. The app returns to its
built-in answers immediately.
