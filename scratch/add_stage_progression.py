with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    # 4. Direct registration details in chat
    if stage in ["CUSTOMER_SIGNUP", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_LOGIN", "USER_TYPE_SELECTION"]:'''

replacement = '''    # 4. Stage progression for User Selection, Account Check, Login, KYC, Tracker
    if stage in ["USER_TYPE_SELECTION", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_LOGIN", "KYC_VERIFICATION", "INSTALLATION_TRACKING"]:
        wf_reply = parse_chat_intents(sid, message)
        if wf_reply:
            sync_workflow_to_session(sid)
            return jsonify({
                "status": "success",
                "session_id": sid,
                "reply": wf_reply,
                "workflow": wf,
                "quick_replies": wf["messages"][-1].get("quick_replies", []) if wf["messages"] else ["Continue"],
                "profile": session["profile"],
                "identified_needs": session["identified_needs"],
                "discovery_status": "in_progress",
                "engine": "Airtel Workflow Engine (Dual-Mode Sync)"
            })

    # 4B. Direct registration details in chat
    if stage in ["CUSTOMER_SIGNUP", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_LOGIN", "USER_TYPE_SELECTION"]:'''

assert target in text, "target not found in app.py"
text = text.replace(target, replacement, 1)

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added stage progression for auth/KYC stages in app.py successfully")
