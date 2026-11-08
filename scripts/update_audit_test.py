with open(r"e:\Airtel\prototype\test_conversational_first_audit.py", "r", encoding="utf-8") as f:
    text = f.read()

target1 = '''    # 2.9 Proceed to Smart KYC via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "GO_TO_STAGE", "payload": {"stage": "KYC_VERIFICATION"}
    }).json()["workflow"]
    assert wf["stage"] == "KYC_VERIFICATION", f"Expected KYC_VERIFICATION, got {wf['stage']}"
    
    # 2.10 Proceed to Live Fulfillment Stepper via GUI'''

replacement1 = '''    # 2.9 Proceed to Smart KYC via GUI
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "GO_TO_STAGE", "payload": {"stage": "KYC_VERIFICATION"}
    }).json()["workflow"]
    assert wf["stage"] == "KYC_VERIFICATION", f"Expected KYC_VERIFICATION, got {wf['stage']}"

    # 2.9b Complete KYC Verification via Specimen Demo
    wf = s.post(f"{BASE}/api/workflow/transition", json={
        "session_id": sess_gui, "action": "VERIFY_KYC_DEMO", "payload": {"gstin": "07AAAAA0000A1Z5"}
    }).json()["workflow"]
    assert wf["kyc"]["status"] in ["VERIFIED", "APPROVED"]
    
    # 2.10 Proceed to Live Fulfillment Stepper via GUI'''

target2 = '''    # 3.7 Chat: Ask to do KYC
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "Let us verify KYC documents"
    }).json()
    wf = r["workflow"]
    assert wf["stage"] == "KYC_VERIFICATION", f"Expected KYC_VERIFICATION, got {wf['stage']}"
    
    # 3.8 Chat: Track order'''

replacement2 = '''    # 3.7 Chat: Ask to do KYC
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "Let us verify KYC documents"
    }).json()
    wf = r["workflow"]
    assert wf["stage"] == "KYC_VERIFICATION", f"Expected KYC_VERIFICATION, got {wf['stage']}"

    # 3.7b Chat: Complete KYC via demo
    r = s.post(f"{BASE}/api/advisor/chat", json={
        "session_id": sess_chat, "message": "Verify specimen demo"
    }).json()
    
    # 3.8 Chat: Track order'''

if target1 in text:
    text = text.replace(target1, replacement1, 1)
if target2 in text:
    text = text.replace(target2, replacement2, 1)

with open(r"e:\Airtel\prototype\test_conversational_first_audit.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated test_conversational_first_audit.py successfully.")
