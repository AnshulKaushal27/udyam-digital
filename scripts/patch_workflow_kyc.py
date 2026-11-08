import os

path = r"e:\Airtel\prototype\customer_workflow_engine.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Fix initial kyc state in get_or_create_workflow
old_init = '''            "kyc": {
                "gstin": "19EOGXH4115Y1ZL",
                "udyam": "UDYAM-MH-00-9516696",
                "applicant_id": "K02",
                "status": "APPROVED",
                "verified": True,
                "signatory_name": "Rajesh Gupta"
            },'''

new_init = '''            "kyc": {
                "gstin": "",
                "udyam": "",
                "applicant_id": None,
                "status": "PENDING",
                "verified": False,
                "signatory_name": "",
                "documents": []
            },'''

if old_init in text:
    text = text.replace(old_init, new_init, 1)
    print("Fixed initial kyc state.")
else:
    print("WARNING: old_init not found!")

# 2. Fix SUBMIT_KYC and VERIFY_KYC_DEMO in transition_workflow
old_actions = '''    elif action in ["VERIFY_KYC_DEMO", "SUBMIT_KYC"]:
        wf["kyc"]["status"] = "VERIFIED"
        wf["kyc"]["gstin"] = payload.get("gstin", "07AAAAA0000A1Z5")
        wf["stage"] = "INSTALLATION_TRACKING"
        wf["messages"].append({
            "sender": "bot",
            "text": "Smart KYC instant verification PASSED! Field engineer Rahul Sharma is assigned to fulfill your order.",
            "quick_replies": [
                {"label": "Track Order Progress", "action": "GO_TO_STAGE", "value": "INSTALLATION_TRACKING"}
            ]
        })'''

new_actions = '''    elif action == "VERIFY_KYC_DEMO":
        wf["kyc"]["status"] = "VERIFIED"
        wf["kyc"]["verified"] = True
        wf["kyc"]["gstin"] = payload.get("gstin", "07AAAAA0000A1Z5")
        wf["stage"] = "INSTALLATION_TRACKING"
        wf["messages"].append({
            "sender": "bot",
            "text": "Smart KYC specimen demo verification PASSED! Specimen test cleared under simulated benchmark.",
            "quick_replies": [
                {"label": "Track Order Progress", "action": "GO_TO_STAGE", "value": "INSTALLATION_TRACKING"}
            ]
        })

    elif action == "SUBMIT_KYC":
        is_appr = payload.get("is_approved") or payload.get("status") in ["APPROVED", "VERIFIED"]
        if is_appr:
            wf["kyc"]["status"] = "VERIFIED"
            wf["kyc"]["verified"] = True
            if payload.get("gstin"):
                wf["kyc"]["gstin"] = payload.get("gstin")
            wf["stage"] = "INSTALLATION_TRACKING"
            wf["messages"].append({
                "sender": "bot",
                "text": "Smart KYC statutory verification PASSED! Field engineer Rahul Sharma is assigned to fulfill your order.",
                "quick_replies": [
                    {"label": "Track Order Progress", "action": "GO_TO_STAGE", "value": "INSTALLATION_TRACKING"}
                ]
            })
        else:
            wf["kyc"]["status"] = payload.get("status", "REVIEW_REQUIRED")
            wf["kyc"]["verified"] = False
            wf["messages"].append({
                "sender": "bot",
                "text": "KYC document submitted but requires review or re-upload. Cannot proceed to installation tracking yet.",
                "quick_replies": [
                    {"label": "📄 Review KYC Documents", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"}
                ]
            })'''

if old_actions in text:
    text = text.replace(old_actions, new_actions, 1)
    print("Fixed SUBMIT_KYC / VERIFY_KYC_DEMO actions.")
else:
    print("WARNING: old_actions not found!")

# 3. Fix GO_TO_STAGE gate for INSTALLATION_TRACKING
old_goto = '''    elif action == "GO_TO_STAGE":
        new_stage = payload.get("stage") or payload.get("value")
        if new_stage in STAGES:'''

new_goto = '''    elif action == "GO_TO_STAGE":
        new_stage = payload.get("stage") or payload.get("value")
        if new_stage == "INSTALLATION_TRACKING":
            kyc_status = wf.get("kyc", {}).get("status", "PENDING")
            if kyc_status not in ["APPROVED", "VERIFIED"]:
                wf["messages"].append({
                    "sender": "bot",
                    "text": "Cannot proceed to installation tracking. Statutory KYC verification has not been approved yet. Please complete document verification first.",
                    "quick_replies": [
                        {"label": "📄 Review KYC Documents", "action": "GO_TO_STAGE", "value": "KYC_VERIFICATION"}
                    ]
                })
                return wf
        if new_stage in STAGES:'''

if old_goto in text:
    text = text.replace(old_goto, new_goto, 1)
    print("Fixed GO_TO_STAGE gate.")
else:
    print("WARNING: old_goto not found!")

# 4. Fix conversational chat handler in KYC_VERIFICATION stage
old_chat = '''    if stage == "KYC_VERIFICATION":
        if any(k in text for k in ["verify", "test", "demo", "rajesh", "specimen", "gstin", "07aaaaa", "approve", "bypass", "done", "next", "proceed", "fulfill", "track", "ok", "okay", "move on", "move ahead", "confirm", "submit", "yes", "haan", "theek hai", "chalo", "aage"]):
            wf["kyc"]["status"] = "VERIFIED"
            wf["kyc"]["gstin"] = "07AAAAA0000A1Z5"
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "INSTALLATION_TRACKING"})
            return "Smart KYC Instant Verification PASSED! Field engineer Rahul Sharma has been dispatched to fulfill your order. Tracking is live on the left panel!"'''

new_chat = '''    if stage == "KYC_VERIFICATION":
        if any(k in text for k in ["demo kyc", "test specimen", "specimen demo", "specimen verify", "07aaaaa"]):
            transition_workflow(session_id, "VERIFY_KYC_DEMO", {"gstin": "07AAAAA0000A1Z5"})
            return "Smart KYC Specimen Demo PASSED! Tested under simulated benchmark. Tracking is live on the left panel!"
        else:
            return "Please upload or capture your KYC document on the left panel, and confirm DPDP statutory consent. Our Smart KYC engine will verify it in real-time."'''

if old_chat in text:
    text = text.replace(old_chat, new_chat, 1)
    print("Fixed chat handler in KYC_VERIFICATION.")
else:
    print("WARNING: old_chat not found!")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated customer_workflow_engine.py.")
