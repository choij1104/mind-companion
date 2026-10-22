# Mind Companion — Google Play build

Free app. Application ID `com.hakoya.mindcompanion`. Publisher: HAKOYA LLC. Target audience 18+.

The store bundle is `android/scripts/build-store.py` run on the repository's `index.html`; the web
app itself is not modified. Differences from the web version:
- Offline: the optional "Conversation" relay (Settings) is left out; answers come from the app's
  built-in answers and the data saved on the device.
- No service worker.
- `android/scripts/native-shim.js` provides the Web Speech API (voice questions, voice notes, spoken
  answers) on top of @capacitor-community/speech-recognition and text-to-speech, and sends backup,
  report and CSV files to the Android share sheet (@capacitor/filesystem, @capacitor/share).

Permissions: RECORD_AUDIO (voice questions and notes, asked the first time the microphone is used),
ACCESS_COARSE/FINE_LOCATION (only the "I'm lost" screen, which puts a map link into a text message
the user sends), INTERNET (Capacitor template; the app makes no network requests).

## Build
GitHub Actions → "Android build (Google Play)". Runs on a push to `android-build` or by manual
dispatch. Produces an **unsigned** App Bundle, kept as a workflow artifact and committed to the
`android-artifacts` branch at `dist/mind-companion-<version>-<code>-unsigned.aab` (`dist/LATEST`
names the newest). versionCode = workflow run number.

## Sign
Upload key for this app: `mindcompanion-upload.p12` (alias `upload`) in Google Drive
`00_CLAUDE_HQ/HAKOYA_Android_UploadKeys_2026-10`, password in the README there.

    jarsigner -keystore mindcompanion-upload.p12 -storetype PKCS12 -signedjar out-signed.aab in-unsigned.aab upload
    jarsigner -verify out-signed.aab
