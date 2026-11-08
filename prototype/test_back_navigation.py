import urllib.request
import json
import os

base_url = "http://127.0.0.1:5000"

def send_transition(session_id, action, payload=None):
    payload = payload or {}
    req = urllib.request.Request(
        f"{base_url}/api/workflow/transition",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"session_id": session_id, "action": action, "payload": payload}).encode("utf-8")
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def send_chat(session_id, msg):
    req = urllib.request.Request(
        f"{base_url}/api/advisor/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"session_id": session_id, "message": msg}).encode("utf-8")
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

print("======================================================================")
print("TESTING BACK BUTTON & PREVIOUS STEP NAVIGATION PIPELINE")
print("======================================================================")

sid = f"sess_test_back_btn_run_{os.urandom(4).hex()}"

# 1. Start at USER_TYPE_SELECTION -> select customer
r1 = send_transition(sid, "SELECT_USER_TYPE", {"user_type": "customer"})
print("[TEST 1] Step forward to CUSTOMER_ACCOUNT_CHECK:", r1["workflow"]["stage"])
assert r1["workflow"]["stage"] == "CUSTOMER_ACCOUNT_CHECK"

# 2. Go back to USER_TYPE_SELECTION
r2 = send_transition(sid, "PREVIOUS_STAGE")
print("[TEST 2] Step backward to USER_TYPE_SELECTION:", r2["workflow"]["stage"])
assert r2["workflow"]["stage"] == "USER_TYPE_SELECTION"

# 3. Advance across multiple stages
send_transition(sid, "SELECT_USER_TYPE", {"user_type": "customer"})
send_transition(sid, "SELECT_ACCOUNT_STATUS", {"status": "new"})
send_transition(sid, "GO_TO_STAGE", {"stage": "BUSINESS_IDENTIFICATION"})
send_transition(sid, "GO_TO_STAGE", {"stage": "REQUIREMENTS_COLLECTION"})
send_transition(sid, "GO_TO_STAGE", {"stage": "PLAN_EXPLORATION"})
r_kyc = send_transition(sid, "GO_TO_STAGE", {"stage": "KYC_VERIFICATION"})
print("[TEST 3] Step forward to KYC_VERIFICATION:", r_kyc["workflow"]["stage"])
assert r_kyc["workflow"]["stage"] == "KYC_VERIFICATION"

# 4. Click Back from KYC -> Goes to PLAN_EXPLORATION
r_back_plan = send_transition(sid, "PREVIOUS_STAGE")
print("[TEST 4] Back from KYC to Plan Exploration:", r_back_plan["workflow"]["stage"])
assert r_back_plan["workflow"]["stage"] == "PLAN_EXPLORATION"

# 5. Click Back from Plan Exploration -> Goes to REQUIREMENTS_COLLECTION
r_back_req = send_transition(sid, "PREVIOUS_STAGE")
print("[TEST 5] Back from Plan to Requirements:", r_back_req["workflow"]["stage"])
assert r_back_req["workflow"]["stage"] == "REQUIREMENTS_COLLECTION"

# 6. Chat conversational 'go back' intent
c_res = send_chat(sid, "go back")
print("[TEST 6] Chat Natural Language 'go back' intent:")
print("  Advisor Reply:", c_res.get("response", "")[:80] + "...")
with urllib.request.urlopen(f"{base_url}/api/workflow/state/{sid}") as r:
    wf = json.loads(r.read().decode())["workflow"]
    print("  Workflow Stage after chat 'go back':", wf["stage"])
    assert wf["stage"] == "BUSINESS_IDENTIFICATION"

# 7. Check HTML includes #btnPrevStage in the template
with urllib.request.urlopen(f"{base_url}/") as r:
    html = r.read().decode("utf-8")
    assert 'id="btnPrevStage"' in html
    assert 'goToPreviousStage()' in html
    print("[TEST 7] HTML DOM contains #btnPrevStage and goToPreviousStage() handler.")

print("\n======================================================================")
print(">>> ALL BACK BUTTON & PREVIOUS STEP TESTS PASSED WITH 100%! <<<")
print("======================================================================")
