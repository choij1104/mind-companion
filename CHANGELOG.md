# Changelog — Mind Companion

## v1.5 — 2026-08-20

The first release since v1.3. It carries both v1.4 and v1.5, which were built but never
published, plus fixes found while preparing this release.

### Added
- **Mind screen** — a daily mood log with five plain choices, and a two-question check-in
  presented as self-reflection, never as a score, a screening result, or a diagnosis.
- **Counseling summary page** — one large-text page of recent moods and answers to bring
  to an appointment.
- **Counseling contact** — the counselor's name, organization, and number, kept with the app.
- **Time-of-day line** on Home, for orientation.
- **Identity answers** — "Who am I?" and "Where do I live?" are answered offline from the
  information saved on the Help screen.
- **Simple Mode** — a reduced interface for someone with more advanced memory difficulty.
- **4-week report** — a printable page of medicine marks, mood, check answers, and points
  worth discussing, for a caregiver or program staff.
- **CSV data file** — the same records as a spreadsheet.
- Spanish and Japanese instructions for the conversation assistant, which previously fell
  back to English.

### Fixed
- Two-button rows no longer push the page sideways on a 320 px screen in any language.
- The service worker returns a clean response instead of failing when an asset is missing
  and the device is offline.
- `sw.js` now caches under `mind-companion-v1.5`, so devices pick up this release instead
  of serving v1.3 from cache.

### Changed
- README now describes the Mind screen, the four languages, and the caregiver tools, and
  states the license correctly as proprietary. It previously said MIT, which contradicted
  the LICENSE file.
- The privacy policy now lists mood entries, mind check answers, and the counselor contact
  among the information stored on the device, and explains what the exported files contain.
- The app manifest description mentions the mind check-in.

### Notes
- Backups exported by v1.3 restore into v1.5 without change. New fields start empty.
- Verified before release: all four translation tables carry identical keys; every screen
  renders in every language at 320, 390, and 768 px with no console errors; the service
  worker registers and the app reloads with the network off; saved data survives a reload.

## v1.3 — 2026-07
Memory aid: voice questions, medicine checklist, contacts, memory notes, emergency
information, four languages, offline shell cache, optional conversation relay.
