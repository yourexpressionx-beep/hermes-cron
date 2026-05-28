import urllib.request, urllib.parse, json, os
from datetime import date
TOKEN=os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
TODAY = date.today().strftime("%Y-%m-%d")
SEARCHES = [
    ("AI Video Gen", "AI video generation latest news 2026 new models pricing"),
    ("AI Image Gen", "AI image generation model updates 2026"),
    ("AI Coding Agents", "Claude Code Codex Gemini CLI updates 2026"),
    ("OpenRouter", "OpenRouter new models pricing 2026"),
    ("fal.ai", "fal ai new models video image 2026"),
    ("YouTube AI", "YouTube AI creator tools 2026"),
]
def ddg(q):
    url = "https://api.duckduckgo.com/?q=" + urllib.parse.quote(q) + "&format=json&no_html=1&skip_disambig=1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        out = []
        if data.get("AbstractText"):
            out.append(data["AbstractText"][:300])
        for t in data.get("RelatedTopics", [])[:3]:
            if isinstance(t, dict) and t.get("Text"):
                out.append(t["Text"][:200])
        return chr(10).join(out[:2]) if out else ""
    except:
        return ""
def send_tg(text):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    body = urllib.parse.urlencode({"chat_id": CHAT, "text": text}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}
report = "Tech Scan - " + TODAY + chr(10) + chr(10)
for label, query in SEARCHES:
    result_ddg = ddg(query)
    if result_ddg:
        report += label + chr(10) + result_ddg + chr(10) + chr(10)
report += "7 AM IST"
if len(report) > 4000:
    for i in range(0, len(report), 4000):
        send_tg(report[i:i+4000])
else:
    send_tg(report)
