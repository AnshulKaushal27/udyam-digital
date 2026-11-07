"""Fix advisor_chat in app.py so it does not bypass discovery and dump bundles prematurely."""
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''    live_reply, live_bundle_id, engine_name = call_live_llm(message, lang)
    
    if live_reply:
        return jsonify({
            "status": "success",
            "session_id": session["session_id"],
            "quote_id": quote_id,
            "reply": live_reply,
            "profile": profile,
            "identified_needs": session["identified_needs"],
            "discovery_status": profile["discovery_status"],
            "bundle": best_bundle,
            "recommendation": rec_result,
            "quote": quote_obj,
            "discovery_complete": is_complete,
            "quick_replies": ["Looks good", "Check Price", "Can I add Wi-Fi?"],
            "engine": engine_name
        })

    # Proactive Sales Consultant Fallback
    fb_text, fb_quick, fb_bundle, fb_complete, fb_why = generate_deterministic_consultant_reply(session, message, lang)
    if not is_complete and not fb_complete:
        return jsonify({
            "status": "success",
            "session_id": session["session_id"],
            "quote_id": None,
            "reply": fb_text,
            "profile": profile,
            "identified_needs": session["identified_needs"],
            "discovery_status": "in_progress",
            "bundle": None,
            "recommendation": None,
            "quote": None,
            "discovery_complete": False,
            "quick_replies": fb_quick,
            "engine": "Airtel Proactive Sales Advisor"
        })'''

replacement = '''    # Consultative Proactive Sales Discovery Logic
    fb_text, fb_quick, fb_bundle, fb_complete, fb_why = generate_deterministic_consultant_reply(session, message, lang)
    
    if not is_complete and not fb_complete:
        return jsonify({
            "status": "success",
            "session_id": session["session_id"],
            "quote_id": None,
            "reply": fb_text,
            "profile": profile,
            "identified_needs": session["identified_needs"],
            "discovery_status": "in_progress",
            "bundle": None,
            "recommendation": None,
            "quote": None,
            "discovery_complete": False,
            "quick_replies": fb_quick,
            "engine": "Airtel Proactive Sales Advisor"
        })'''

content_clean = content.replace('\r\n', '\n')
target_clean = target.replace('\r\n', '\n')
replacement_clean = replacement.replace('\r\n', '\n')

assert target_clean in content_clean, "Target block not found"
content_clean = content_clean.replace(target_clean, replacement_clean, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(content_clean)

print("advisor_chat updated successfully!")
