def main():
    # 1. Update customer_workflow_engine.py
    wf_path = "prototype/customer_workflow_engine.py"
    with open(wf_path, "r", encoding="utf-8") as f:
        wf_content = f.read()

    wf_target = '''    if stage == "USER_TYPE_SELECTION":
        if any(k in text for k in ["business", "business owner", "customer", "merchant", "dukaan", "shop", "own a business", "store owner", "businessman", "entrepreneur", "retailer", "client", "msme", "smb", "1", "option 1"]) and not any(w in text for w in ["airtel employee", "internal staff", "airtel team"]):
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "customer"})
            return "Noted! Welcome, business owner. Are you already an Airtel Business customer?"

        if any(k in text for k in ["employee", "staff", "airtel team", "internal", "support", "agent", "2", "option 2"]):
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "employee"})
            return "Welcome Airtel Team! You can access the Operations Control Portal directly in Demo Mode."'''

    wf_replacement = '''    if stage == "USER_TYPE_SELECTION":
        if any(k in text for k in ["business", "business owner", "customer", "merchant", "dukaan", "shop", "store", "grocery", "run a", "own a business", "store owner", "businessman", "entrepreneur", "retailer", "client", "msme", "smb", "1", "option 1"]) and not any(w in text for w in ["airtel employee", "internal staff", "airtel team"]):
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "customer"})
            return "Noted! Welcome, business owner. Are you already an Airtel Business customer?"

        if any(k in text for k in ["airtel employee", "internal staff", "airtel team", "airtel staff", "employee portal", "control portal"]) or text in ["employee", "staff", "airtel", "2", "option 2"]:
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "employee"})
            return "Welcome Airtel Team! You can access the Operations Control Portal directly in Demo Mode."'''

    assert wf_target in wf_content, "wf_target not found"
    wf_content = wf_content.replace(wf_target, wf_replacement, 1)
    with open(wf_path, "w", encoding="utf-8") as f:
        f.write(wf_content)
    print("Successfully updated customer_workflow_engine.py user type logic")

    # 2. Update app.py
    app_path = "prototype/app.py"
    with open(app_path, "r", encoding="utf-8") as f:
        app_content = f.read()

    app_target = '''        if wf_reply:
            sync_workflow_to_session(sid)
            b_id = wf.get("recommendation", {}).get("bundle_id")
            bundle_data = HERO_BUNDLES_MASTER.get(b_id) if b_id else None
            return jsonify({
                "status": "success",
                "session_id": sid,
                "reply": wf_reply,
                "workflow": wf,
                "quick_replies": wf["messages"][-1].get("quick_replies", []) if wf["messages"] else ["Continue"],
                "profile": session["profile"],
                "identified_needs": session["identified_needs"],
                "discovery_status": "in_progress",
                "bundle": bundle_data,
                "engine": "Airtel Workflow Engine (Dual-Mode Sync)"
            })'''

    app_replacement = '''        if wf_reply:
            sync_workflow_to_session(sid)
            b_id = wf.get("recommendation", {}).get("bundle_id")
            bundle_data = HERO_BUNDLES_MASTER.get(b_id) if b_id else None
            existing_qid = next((qid for qid, q in SHARED_QUOTES.items() if q.get("session_id") == sid), None)
            active_quote = SHARED_QUOTES.get(existing_qid) if existing_qid else None
            return jsonify({
                "status": "success",
                "session_id": sid,
                "reply": wf_reply,
                "workflow": wf,
                "quick_replies": wf["messages"][-1].get("quick_replies", []) if wf["messages"] else ["Continue"],
                "profile": session["profile"],
                "identified_needs": session["identified_needs"],
                "discovery_status": "in_progress",
                "bundle": bundle_data,
                "quote": active_quote,
                "quote_id": existing_qid,
                "engine": "Airtel Workflow Engine (Dual-Mode Sync)"
            })'''

    assert app_target in app_content, "app_target not found"
    app_content = app_content.replace(app_target, app_replacement, 1)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_content)
    print("Successfully updated app.py Dual-Mode Sync response with quote")

if __name__ == "__main__":
    main()
