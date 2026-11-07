"""Update advisor_chat_stream and advisor_chat in prototype/app.py"""
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update advisor_chat_stream preamble to detect language and billing intent
old_chat_stream_preamble = '''    session = get_or_create_session(sid, raw_cat, lang)
    profile = session["profile"]

    # Extract user input and update deterministic profile
    last_user_text = ""
    for m in reversed(messages):
        if m.get("role") in ["user", "customer"]:
            last_user_text = m.get("content") or m.get("text", "")
            break

    if last_user_text:
        extract_and_update_profile(session, last_user_text)'''

new_chat_stream_preamble = '''    session = get_or_create_session(sid, raw_cat, lang)
    profile = session["profile"]

    # Extract user input and update deterministic profile
    last_user_text = ""
    for m in reversed(messages):
        if m.get("role") in ["user", "customer"]:
            last_user_text = m.get("content") or m.get("text", "")
            break

    # Natural Language Switch Detection
    if last_user_text:
        detected_lang = detect_natural_language_switch(last_user_text)
        if detected_lang:
            lang = detected_lang
            session["profile"]["preferred_language"] = lang
        # Update billing/invoicing intent & customer response classification
        detect_billing_and_invoicing_intent(last_user_text, session)
        extract_and_update_profile(session, last_user_text)'''

assert old_chat_stream_preamble in content, "old_chat_stream_preamble not found"
content = content.replace(old_chat_stream_preamble, new_chat_stream_preamble, 1)

# 2. Update fallback generator in advisor_chat_stream
old_fallback_gen = '''        # Fallback generator if Groq was unavailable or failed
        if not groq_success:
            is_complete = check_discovery_completion(profile, session["identified_needs"], user_count, last_user_text)

            if btype == "kirana":
                if not is_complete and user_count <= 1:
                    text = "Samajh gaya. Aapki dukaan par UPI payments aur POS machine use karte hain?"
                    quick = ["Yes, both UPI & POS", "Only QR payments", "POS card machine", "Cash mainly"]
                elif not is_complete and user_count == 2:
                    text = "Theek hai. Internet slow hone par evening rush me payments rukte hain kya?"
                    quick = ["Yes, evening me rukte hain", "Disconnections happen", "Speed slow rehti hai", "No issues"]
                else:
                    text = "Understood. Aapke liye reliable AirFiber ke saath automatic 4G backup best rahega taaki UPI kabhi na ruke."
                    quick = ["View Package Details", "Check Installation SLA", "Can I add static IP?"]
            elif btype == "clinic":
                if not is_complete and user_count <= 1:
                    text = "Samajh gaya doctor saab. Patient files aur medical records ka secure cloud backup zaroori hai?"
                    quick = ["Yes, 1TB backup needed", "Only fast Wi-Fi", "Need guest Wi-Fi for patients", "Billing suite too"]
                else:
                    text = "Understood! Clinic Suite with 300 Mbps symmetrical fiber and 1TB encrypted cloud backup is ideal for your practice."
                    quick = ["View Package Details", "Check Installation SLA", "Book Appointment"]
            elif btype == "multisite":
                if not is_complete and user_count <= 1:
                    text = "Got it. Do you need centralized CCTV monitoring and SD-WAN failover across your branches on a single bill?"
                    quick = ["Yes, CCTV & SD-WAN both", "Single bill is critical", "Need CCTV mainly", "Just fast internet"]
                else:
                    text = "Understood! Multi-Site Retail Pro links all branches with 1 Gbps fiber, SD-WAN, and 4x Cloud CCTV."
                    quick = ["View Package Details", "Check Installation SLA", "Request Site Survey"]
            else: # manufacturer
                if not is_complete and user_count <= 1:
                    text = "Understood. Do you require dedicated uncompressed leased line bandwidth with static IP for ERP?"
                    quick = ["Yes, 1:1 Leased Line", "Static IP for ERP", "Machine IoT sensors", "All of these"]
                else:
                    text = "Understood. The Small Manufacturing Suite with uncompressed leased line and machine IoT telemetry is the right fit."
                    quick = ["View Package Details", "Check Installation SLA", "Talk to Enterprise Team"]

            for w in text.split(" "):
                yield f"data: {json.dumps({'type': 'chunk', 'text': w + ' '})}\\n\\n"
                time.sleep(0.04)

            parsed_meta = {
                "quick_replies": quick,
                "recommend_bundle": target_bundle_id if is_complete else None,
                "discovery_complete": is_complete,
                "why_brief": bundle_data["why"]
            }'''

new_fallback_gen = '''        # Fallback generator if Groq was unavailable or failed
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

assert old_fallback_gen in content, "old_fallback_gen not found"
content = content.replace(old_fallback_gen, new_fallback_gen, 1)

# 3. Update is_complete check in advisor_chat_stream
old_check_comp = '''            # Re-evaluate discovery completion deterministically
            is_complete = check_discovery_completion(profile, session["identified_needs"], user_count, last_user_text)'''

new_check_comp = '''            # Re-evaluate discovery completion deterministically
            is_complete = check_discovery_completion(profile, session["identified_needs"], user_count, last_user_text, session)'''

assert old_check_comp in content, "old_check_comp not found"
content = content.replace(old_check_comp, new_check_comp, 1)

# 4. Update final_meta in advisor_chat_stream to pass detected_language and billing_intent
old_final_meta = '''        final_meta = {
            "session_id": session["session_id"],
            "quote_id": quote_id,
            "business_type": btype,
            "profile": profile,
            "identified_needs": session["identified_needs"],
            "discovery_status": profile["discovery_status"],
            "quick_replies": parsed_meta.get("quick_replies", []),
            "recommend_bundle": target_bundle_id if is_finished else None,
            "why_brief": parsed_meta.get("why_brief") or current_bundle_data.get("why_brief", current_bundle_data.get("why", "")),
            "engine": "Groq (GPT-OSS-120B Live)" if groq_success else "Airtel Rule Engine (Fallback)",
            "recommendation": rec_result if is_finished else None,
            "quote": quote_obj if is_finished else None
        }'''

new_final_meta = '''        final_meta = {
            "session_id": session["session_id"],
            "quote_id": quote_id,
            "business_type": btype,
            "profile": profile,
            "identified_needs": session["identified_needs"],
            "discovery_status": profile["discovery_status"],
            "quick_replies": parsed_meta.get("quick_replies", []),
            "recommend_bundle": target_bundle_id if is_finished else None,
            "why_brief": parsed_meta.get("why_brief") or current_bundle_data.get("why_brief", current_bundle_data.get("why", "")),
            "engine": "Groq (GPT-OSS-120B Live)" if groq_success else "Airtel Proactive Sales Advisor",
            "recommendation": rec_result if is_finished else None,
            "quote": quote_obj if is_finished else None,
            "detected_language": lang,
            "billing_intent": session.get("billing_intent", {}),
            "preference_tracking": session.get("preference_tracking", {})
        }'''

assert old_final_meta in content, "old_final_meta not found"
content = content.replace(old_final_meta, new_final_meta, 1)

# 5. Update advisor_chat (non-streaming)
old_advisor_chat = '''@app.route("/api/advisor/chat", methods=["POST"])
def advisor_chat():
    """Standard non-streaming conversational endpoint with deterministic recommendation & quote persistence."""
    data = request.json or {}
    sid = data.get("session_id")
    message = data.get("message", "").strip()
    raw_cat = data.get("category") or data.get("profile", {}).get("business_type", message)
    lang = data.get("language", data.get("profile", {}).get("preferred_language", "en")).lower()
    
    session = get_or_create_session(sid, raw_cat, lang)
    profile = session["profile"]

    if message:
        extract_and_update_profile(session, message)

    btype = profile["business_type"]
    msg_count = len(session["messages"]) + 1
    is_complete = check_discovery_completion(profile, session["identified_needs"], msg_count, message)
    profile["discovery_status"] = "complete" if is_complete else "in_progress"'''

new_advisor_chat = '''@app.route("/api/advisor/chat", methods=["POST"])
def advisor_chat():
    """Standard non-streaming conversational endpoint with deterministic recommendation & quote persistence."""
    data = request.json or {}
    sid = data.get("session_id")
    message = data.get("message", "").strip()
    raw_cat = data.get("category") or data.get("profile", {}).get("business_type", message)
    lang = data.get("language", data.get("profile", {}).get("preferred_language", "en")).lower()
    
    session = get_or_create_session(sid, raw_cat, lang)
    profile = session["profile"]

    if message:
        detected_lang = detect_natural_language_switch(message)
        if detected_lang:
            lang = detected_lang
            session["profile"]["preferred_language"] = lang
        detect_billing_and_invoicing_intent(message, session)
        extract_and_update_profile(session, message)

    btype = profile["business_type"]
    msg_count = len(session["messages"]) + 1
    is_complete = check_discovery_completion(profile, session["identified_needs"], msg_count, message, session)
    profile["discovery_status"] = "complete" if is_complete else "in_progress"'''

assert old_advisor_chat in content, "old_advisor_chat not found"
content = content.replace(old_advisor_chat, new_advisor_chat, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Part 2 streaming & advisor_chat updates applied to app.py successfully!")
