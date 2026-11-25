# Syncerely site

Public files for the Syncerely Android app, served by GitHub Pages at
https://abdo-1998.github.io/syncerely-site/

- `messages.json`: important messages the app shows on Home.
- `index.html`: a plain front page.

## Sending a message to every user

The app reads `messages.json` at most once a day (when it opens, and after a background sync). Nothing
about the user is sent. Changes go live about a minute after you save, and users see them at their next
daily read.

**From a phone or computer:**

1. Open https://github.com/abdo-1998/syncerely-site/edit/main/messages.json (sign in to GitHub).
2. Add a message inside the `[ ]` (copy one of the examples below).
3. Tap **Commit changes**.

To take a message down, delete it from the list and commit again. An empty list is fine:

```json
{
  "messages": []
}
```

### A normal message

A card on Home under the status card, with a close X. Once closed, it stays closed on that phone.

```json
{
  "messages": [
    {
      "id": "2026-12-drive-slow",
      "title": "Google Drive is slow today",
      "text": "Google says uploads may take longer until tonight. Nothing is lost; syncs carry on.",
      "expires": "2026-12-02"
    }
  ]
}
```

### A critical message

The card in the warning colour, with an **Update** button when `link` is the Play Store (otherwise
**Read more**). It also arrives as one notification. It has no close X: it goes away when it no longer
applies, so set `maxVersion` to the last affected version.

```json
{
  "messages": [
    {
      "id": "2026-12-onedrive-bug",
      "severity": "critical",
      "title": "Please update Syncerely",
      "text": "A bug in this version can stop OneDrive uploads. Version 1.0.3 fixes it.",
      "maxVersion": 24,
      "link": "https://play.google.com/store/apps/details?id=com.abdosdevstudio.syncerely"
    }
  ]
}
```

### Every field

| Field | Needed | What it does |
|---|---|---|
| `id` | yes | Any unique name. A new id is a new message (closed ones stay closed by id). |
| `title` | yes | The bold first line. |
| `text` | yes | One or two sentences. |
| `severity` | no | `"normal"` (default) or `"critical"`. |
| `minVersion` / `maxVersion` | no | Only these app version codes (both ends included). The version code is the number in brackets in Settings' Report a problem summary, e.g. `118`. |
| `link` | no | A page to open. A Play Store link makes the button say **Update**. |
| `expires` | no | Last day it shows, as `"yyyy-mm-dd"`. |

### Forcing an update

Add `"forceUpdateBelow": 25` next to `"messages"` and every install older than version code 25 gets
Play's full-screen update (only for installs from Play). Use it only for a fix that matters.

```json
{
  "forceUpdateBelow": 25,
  "messages": []
}
```

### Check before you save

The whole file must stay valid JSON: commas between messages, none after the last, double quotes. If
the file is broken the app shows nothing (it never crashes), so a mistake hides messages rather than
breaking the app. Paste it into https://jsonlint.com to check if unsure.
