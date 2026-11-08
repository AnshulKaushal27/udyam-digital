def main():
    path = "prototype/app.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    target = '''        if wf_reply:
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
            })'''

    replacement = '''        if wf_reply:
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

    assert target in content, "Target block not found"
    new_content = content.replace(target, replacement, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated app.py with bundle in Dual-Mode Sync response")

if __name__ == "__main__":
    main()
