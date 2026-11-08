import requests

sid = "sess_test_check_msgs"
# 1. State
requests.get(f"http://127.0.0.1:5000/api/workflow/state/{sid}")
requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "GO_TO_STAGE",
    "payload": {"stage": "REQUIREMENTS_COLLECTION"}
})
requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "TOGGLE_REQUIREMENT",
    "payload": {"requirement": "broadband_speed"}
})
r = requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "GO_TO_STAGE",
    "payload": {"stage": "PLAN_EXPLORATION", "label": "Generate Digital Bundle"}
})
wf = r.json().get("workflow", {})
print("Workflow stage:", wf.get("stage"))
print("Workflow messages count:", len(wf.get("messages", [])))
for m in wf.get("messages", [])[-3:]:
    print(" -", m.get("sender"), ":", m.get("text")[:60])
