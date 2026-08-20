# Privacy Policy

**Mind Companion** · Last updated: August 2026

## Short version

The app collects nothing. Everything typed or spoken into it stays on the device.

## What is stored

The following are saved in the browser's local storage on the device, and nowhere else:

- Medicine names, times, notes, and which items were marked as taken
- Contact names, phone numbers, and roles
- Memory notes
- Personal information entered on the Help screen (name, address, conditions, allergies, blood type)
- Daily mood entries, and the answers to the two-question mind check (the most recent 24 are kept)
- The counselor's name, organization, and phone number, if entered
- Preferences (language, text size, Simple Mode)

## What is not done

- No account or sign-in
- No analytics, tracking, cookies, or advertising
- No transmission of any entered information to any server
- No sharing with third parties

## Reports and exports

The counseling summary page, the 4-week report, the CSV data file, and the backup file are
created on the device and saved to the device. Nothing is uploaded when any of them is made.
Once a file has been saved, shared, or printed, it is an ordinary document outside the app's
control — the 4-week report and the CSV contain mood entries, mind check answers, and medicine
marks, so treat them as personal health information.

## Conversation (optional, off by default)

The app ships with conversation turned off and works entirely on the device.

If a connection address is entered in Settings, each question is sent to a relay controlled by
whoever set the app up, and from there to Anthropic's API to produce a reply. To make replies
accurate, the message is accompanied by what is saved in the app: medicine, contacts, memory
notes, the personal details on the Help screen, the counselor's contact if entered, and the
mood recorded today. This is transmitted only at the moment a
question is asked, and only while a connection address is set.

Clearing the connection address in Settings stops all of this immediately.

## Voice input

Voice input uses the browser's built-in Web Speech API. On some browsers — notably Chrome —
speech recognition is processed by the browser vendor's servers, which means the audio of what
is spoken while the microphone button is active may be sent to that vendor for transcription.
That is a function of the browser, not of this app: the app receives only the resulting text
and stores it on the device. Anyone uncomfortable with this can use **Type a question instead**
and never press the microphone.

Spoken output uses the device's built-in speech synthesis and sends nothing anywhere.

## Data retention and loss

Information stays until deleted in the app or until the browser's data is cleared.
Clearing browser data, using private browsing, uninstalling the browser, or replacing the phone
will erase it permanently. There is no backup on any server.

Use **Settings → Save a backup file** to export a copy, and keep that file somewhere safe.
The backup is an ordinary unencrypted JSON file — treat it like any document containing
personal and health information.

## Children

The app is not directed at children.

## Contact

Questions about this policy: open an issue at
https://github.com/choij1104/mind-companion/issues

© 2026 Jae Hyek Choi / HAKOYA LLC
