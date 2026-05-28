import urllib.request, urllib.parse, json, sys, re, os
from datetime import date

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
TODAY = date.today().strftime("%Y-%m-%d")

SEARCHES = [
    ("AI Video Gen", "AI video generation latest news 2026"),
    ("AI Image Gen", "AI image generation model updates 2026"),
    ("AI Coding Agents", "Claude Code Codex AI coding updates 2026"),
    ("OpenRouter", "OpenRouter new models pricing 2026"),
    ("fal.ai", "fal ai new models video image 2026"),
    ("YouTube AI", "YouTube AI creator tools 2026"),
]

def ddg(q):
    try:
        url = "https://api.duckduckgo.com/?q=" + urllib.parse.quote(q) + "&format=json&no_html=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.load(r)
        if d.get("AbstractText"):
            return d["AbstractText"][:250]
        for t in d.get("RelatedTopics", [])[:2]:
            if isinstance(t, dict) and t.get("Text"):
                return t["Text"][:200]
        return ""
    except:
        return ""

def send(text):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    body = urllib.parse.urlencode({"chat_id": CHAT, "text": text}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r).get("ok", False)
    except:
        return False

lines = ["Tech Scan - " + TODAY, ""]
for label, q in SEARCHES:
    r = ddg(q)
    if r:
        lines.append(label + ":")
        lines.append(r)
        lines.append("")
    else:
        lines.append(label + ": No results")
        lines.append("")
lines.append("7 AM IST")

msg = "\n".join(lines)
ok = send(msg)
print("Sent:", ok)
if not ok:
    sys.exit(1)
