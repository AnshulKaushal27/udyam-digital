import requests

sid = "sess_test_send_click"
# 1. Initialize workflow
res0 = requests.get(f"http://127.0.0.1:5000/api/workflow/state/{sid}")
print("Initial stage:", res0.json().get("workflow", {}).get("stage"))

# 2. Transition to REQUIREMENTS_COLLECTION
res1 = requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "GO_TO_STAGE",
    "payload": {"stage": "REQUIREMENTS_COLLECTION"}
})
print("Stage after reqs:", res1.json().get("workflow", {}).get("stage"))

# 3. Add requirement broadband_speed
res2 = requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "TOGGLE_REQUIREMENT",
    "payload": {"requirement": "broadband_speed"}
})
print("Reqs:", res2.json().get("workflow", {}).get("discovery", {}).get("requirements"))

# 4. Click Send with empty input (which calls GO_TO_STAGE PLAN_EXPLORATION)
res3 = requests.post("http://127.0.0.1:5000/api/workflow/transition", json={
    "session_id": sid,
    "action": "GO_TO_STAGE",
    "payload": {"stage": "PLAN_EXPLORATION", "label": "Generate Digital Bundle"}
})
print("Res 3 status:", res3.status_code)
print("Res 3 workflow stage:", res3.json().get("workflow", {}).get("stage"))
