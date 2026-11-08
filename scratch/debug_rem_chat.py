import urllib.request
import json

BASE_URL = "http://127.0.0.1:5000"

def post_json(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data).encode("utf-8")
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

sid = "sess_debug_rem_cctv"
post_json("/api/workflow/transition", {"session_id": sid, "action": "SELECT_USER_TYPE", "payload": {"user_type": "customer"}})
post_json("/api/workflow/transition", {"session_id": sid, "action": "SELECT_CATEGORY", "payload": {"category": "kirana"}})
post_json("/api/workflow/transition", {"session_id": sid, "action": "TOGGLE_REQUIREMENT", "payload": {"requirement": "cctv_security"}})

res = post_json("/api/advisor/chat", {"session_id": sid, "message": "remove cctv", "language": "en"})
print("Reply:", res.get("reply"))
print("Interpretation:", res.get("interpretation"))
print("Active addons after remove:", res.get("workflow", {}).get("recommendation", {}).get("active_addons"))
print("Discovery reqs after remove:", res.get("workflow", {}).get("discovery", {}).get("requirements"))
