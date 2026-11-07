"""Reconcile advisor_chat and advisor_chat_stream in prototype/app.py to satisfy both new proactive sales features and existing regression suites."""
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update fallback generator in advisor_chat_stream
old_fallback = '''        # Fallback generator if Groq was unavailable or failed
        if not groq_success:
            fb_text, fb_quick, fb_bundle, fb_complete, fb_why = generate_deterministic_consultant_reply(session, last_user_text, lang)
            for w in fb_text.split(" "):
                yield f"data: {json.dumps({'type': 'chunk', 'text': w + ' '})}\\n\\n"
                time.sleep(0.02)

            parsed_meta = {
                "quick_replies": fb_quick,
                "recommend_bundle": fb_bundle if fb_complete else None,
                "discovery_complete": fb_complete,
                "why_brief": fb_why
            }'''

new_fallback = '''        # Fallback generator if Groq was unavailable or failed
        if not groq_success:
            is_comp = check_discovery_completion(profile, session["identified_needs"], user_count, last_user_text, session)
            fb_text, fb_quick, fb_bundle, fb_complete, fb_why = generate_deterministic_consultant_reply(session, last_user_text, lang)
            is_fin = is_comp or fb_complete

            for w in fb_text.split(" "):
                yield f"data: {json.dumps({'type': 'chunk', 'text': w + ' '})}\\n\\n"
                time.sleep(0.01)

            parsed_meta = {
                "quick_replies": fb_quick,
                "recommend_bundle": (fb_bundle or target_bundle_id) if is_fin else None,
                "discovery_complete": is_fin,
                "why_brief": fb_why or bundle_data.get("why", "")
            }'''

assert old_fallback in content, "old_fallback not found"
content = content.replace(old_fallback, new_fallback, 1)

# 2. Update advisor_chat (POST /api/advisor/chat)
old_chat = '''    # Consultative Proactive Sales Discovery Logic
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
        })

    return jsonify({
        "status": "success",
        "session_id": session["session_id"],
        "quote_id": quote_id,
        "reply": fb_text,
        "profile": profile,
        "identified_needs": session["identified_needs"],
        "discovery_status": "complete",
        "bundle": best_bundle,
        "recommendation": rec_result,
        "quote": quote_obj,
        "discovery_complete": True,
        "quick_replies": fb_quick,
        "engine": "Airtel Proactive Sales Advisor"
    })'''

new_chat = '''    # Consultative Proactive Sales Discovery Logic
    fb_text, fb_quick, fb_bundle, fb_complete, fb_why = generate_deterministic_consultant_reply(session, message, lang)
    is_finished = is_complete or fb_complete

    # For billing workflow in progress, keep discovery_complete False
    if session.get("billing_intent", {}).get("active") and not is_finished:
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
        })

    return jsonify({
        "status": "success",
        "session_id": session["session_id"],
        "quote_id": quote_id,
        "reply": fb_text,
        "profile": profile,
        "identified_needs": session["identified_needs"],
        "discovery_status": "complete" if is_finished else "in_progress",
        "bundle": best_bundle,
        "recommendation": rec_result,
        "quote": quote_obj,
        "discovery_complete": is_finished,
        "quick_replies": fb_quick,
        "engine": "Airtel Proactive Sales Advisor"
    })'''

assert old_chat in content, "old_chat not found"
content = content.replace(old_chat, new_chat, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Reconciliation applied to prototype/app.py successfully!")
