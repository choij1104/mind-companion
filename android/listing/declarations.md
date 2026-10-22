# Mind Companion — Play Console declarations (answers prepared from the store build)

## App access
All functionality is available without special access (no login).

## Ads
No ads.

## Content rating (IARC) — category "All other app types"
Every question **No** (no violence, fear, sexuality, gambling, profanity, drugs, crude humor;
no user interaction/content sharing; no online content; no age-restricted products; does not share
the user's location with other users — the "I am lost" text is sent by the user to a contact they
choose through the phone's own messaging app; no digital purchases; no rewards; not a browser;
not primarily news/education). Expected: Everyone / PEGI 3.

## Target audience
18 and over only. Not appealing to children.

## Data safety
- Does the app collect or share any required user data types? **No.**
  Reasoning: the store build makes no network requests; everything is stored on the device.
  Voice input is converted to text by the phone's system speech-recognition service (not by code
  that sends data to HAKOYA LLC); the app receives only text. Location is read only when the user
  presses "I am lost" and is placed into an SMS the user sends themselves.
- Is all data encrypted in transit? Not applicable (no data leaves the app).
- Can users request deletion? Data is on the device; deleting the app or using Settings → Reset deletes it.

## Health apps declaration
Features: medication reminders/tracking (on-device), mood tracking / mental wellness check-in
(on-device), emergency information. Not a medical device, no diagnosis or treatment.

## Permissions to explain if asked
- RECORD_AUDIO — voice questions and voice notes (asked the first time the microphone is used)
- ACCESS_COARSE/FINE_LOCATION — only the "I am lost" button
- INTERNET — present in the Capacitor template; the app makes no network requests

## Advertising ID
The app does not use the advertising ID.

## Government apps / Financial features
Not a government app. No financial features.
