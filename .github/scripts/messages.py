"""Turns a "Send a message" or "Remove a message" issue into a change to messages.json.

Reads the issue body (GitHub's issue-form layout: "### Label" then the answer) from the ISSUE_BODY
environment variable, never from the command line, so nothing in it is run. Prints one line for the
closing comment; exits 1 with the reason when the issue can't be used.
"""

import datetime
import json
import os
import re
import sys

FILE = "messages.json"
PLAY = "https://play.google.com/store/apps/details?id=com.abdosdevstudio.syncerely"


def fields(body):
    """{label: answer} from an issue-form body; empty answers ("_No response_") left out."""
    out = {}
    for block in re.split(r"^### ", body or "", flags=re.M)[1:]:
        label, _, answer = block.partition("\n")
        answer = answer.strip()
        if answer and answer != "_No response_":
            out[label.strip()] = answer
    return out


def load():
    try:
        with open(FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    data.setdefault("messages", [])
    return data


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def fail(reason):
    print(reason)
    sys.exit(1)


def send(form, number):
    title, text = form.get("Title", ""), form.get("Text", "")
    if not title or not text:
        fail("A message needs a title and a text.")
    if len(title) > 80 or len(text) > 400:
        fail("Keep the title under 80 characters and the text under 400.")
    message = {"id": f"m{number}-{datetime.date.today().isoformat()}", "title": title, "text": " ".join(text.split())}
    if form.get("How important", "Normal").lower().startswith("critical"):
        message["severity"] = "critical"
    link = form.get("Link (optional)", "")
    if link:
        if link.lower() == "play":
            link = PLAY
        if not link.startswith("https://"):
            fail("The link must start with https://, or be the word play.")
        message["link"] = link
    expires = form.get("Last day it shows (optional)", "")
    if expires:
        try:
            datetime.date.fromisoformat(expires)
        except ValueError:
            fail("The last day must look like 2026-12-02.")
        message["expires"] = expires
    versions = form.get("Only these app versions (optional)", "").replace(" ", "")
    if versions:
        match = re.fullmatch(r"(\d*)-(\d*)|(\d+)", versions)
        if not match:
            fail('Versions must look like "20-24", "-24", "25-" or "24".')
        low, high, one = match.groups()
        if one:
            low = high = one
        if low:
            message["minVersion"] = int(low)
        if high:
            message["maxVersion"] = int(high)
    data = load()
    data["messages"].append(message)
    save(data)
    kind = "critical message" if message.get("severity") == "critical" else "message"
    print(f"Sent: this {kind} (id `{message['id']}`) is live; phones show it at their next daily check.")


def remove(form):
    target = form.get("Message id", "").strip().strip("`")
    data = load()
    before = len(data["messages"])
    if target.lower() == "all":
        data["messages"] = []
    else:
        data["messages"] = [m for m in data["messages"] if m.get("id") != target]
    if len(data["messages"]) == before:
        fail(f"No message has the id `{target}`. The live ones are listed in messages.json.")
    save(data)
    print(f"Removed {before - len(data['messages'])} message(s). Phones drop them at their next daily check.")


if __name__ == "__main__":
    form = fields(os.environ.get("ISSUE_BODY", ""))
    if os.environ.get("ACTION") == "remove":
        remove(form)
    else:
        send(form, os.environ.get("ISSUE_NUMBER", "0"))
