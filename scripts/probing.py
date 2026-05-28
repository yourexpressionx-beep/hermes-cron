import urllib.request, urllib.parse, json, os
from datetime import date

TOKEN=*** = os.environ["TELEGRAM_CHAT_ID"]

QUESTIONS = [
    "What is the one thing in your dev workflow that frustrates you most?",
    "If you could automate one boring task today what would it be?",
    "What is a tool you tried recently that surprised you?",
    "Which client project is taking the most mental energy right now?",
    "What is something you have been putting off learning?",
    "YouTube progress - did you film or edit anything this week?",
    "If budget was not an issue what would you build this month?",
    "What is the last tutorial or course you actually finished?",
    "Any new revenue stream ideas?",
    "What is your biggest bottleneck in shipping faster?",
    "What is a skill you wish you had 6 months ago?",
    "How do you decide which client project to prioritize?",
]

q = QUESTIONS[date.today().timetuple().tm_yday % len(QUESTIONS)]
msg = "Good morning Puneet!\n\nDaily Check-in\n\n" + q + "\n\nJust reply here."

url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
body = urllib.parse.urlencode({"chat_id": CHAT, "text": msg}).encode()
req = urllib.request.Request(url, data=body, method="POST")
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = json.loads(r.read())
        print("Telegram response:", resp)
        if not resp.get("ok"):
            print("FAILED!")
except Exception as e:
    print("Error:", e)
