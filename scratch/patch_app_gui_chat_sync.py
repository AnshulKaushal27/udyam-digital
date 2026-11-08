import re

with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update customer_workflow_engine imports
wf_import_target = """from customer_workflow_engine import (

    get_or_create_workflow,

    authenticate_customer,

    register_customer,

    transition_workflow,

    parse_chat_intents,

    get_i18n_text,

    WORKFLOW_SESSIONS,

    MOCK_CUSTOMERS

)"""

wf_import_replacement = """from customer_workflow_engine import (
    get_or_create_workflow,
    authenticate_customer,
    register_customer,
    transition_workflow,
    parse_chat_intents,
    get_i18n_text,
    WORKFLOW_SESSIONS,
    MOCK_CUSTOMERS,
    get_visible_gui_options,
    get_eligible_catalogue_options,
    extract_signup_details,
    _recalculate_workflow_quote,
    STAGES
)"""

assert wf_import_target in text, "wf_import_target not found in app.py"
text = text.replace(wf_import_target, wf_import_replacement, 1)

# 2. Update conversational_ai imports
conv_import_target = """from conversational_ai import (

    OFFICIAL_CATALOGUE,

    detect_natural_language_switch,

    classify_user_response,

    handle_indecision_policy,

    get_or_create_preference_state,

    detect_billing_and_invoicing_intent,

    validate_catalogue_eligibility,

    build_proactive_sales_prompt,

    generate_deterministic_consultant_reply,

    parse_quote_action_intent

)"""

conv_import_replacement = """from conversational_ai import (
    OFFICIAL_CATALOGUE,
    detect_natural_language_switch,
    classify_user_response,
    handle_indecision_policy,
    get_or_create_preference_state,
    detect_billing_and_invoicing_intent,
    validate_catalogue_eligibility,
    build_proactive_sales_prompt,
    generate_deterministic_consultant_reply,
    parse_quote_action_intent,
    build_unified_advisor_prompt,
    interpret_user_intent_fallback,
    interpret_user_intent_with_context,
    set_test_mock_llm
)"""

assert conv_import_target in text, "conv_import_target not found in app.py"
text = text.replace(conv_import_target, conv_import_replacement, 1)

# 3. Add sync_workflow_to_session helper right above api_workflow_transition
sync_helper_code = '''
def sync_workflow_to_session(session_id: str):
    """
    Maintains authoritative bidirectional synchronization between
    Workflow Engine state (GUI) and Customer Session state (Chat/Advisor).
    """
    if not session_id:
        return None
    wf = get_or_create_workflow(session_id)
    cat = wf.get("discovery", {}).get("business_type", "kirana")
    lang = wf.get("language", "en")
    session = get_or_create_session(session_id, cat, lang)

    # 1. Sync business profile & language
    session["profile"]["business_type"] = cat
    session["profile"]["preferred_language"] = lang
    if wf.get("customer", {}).get("name") and wf["customer"]["name"] != "Valued Business Owner":
        session["profile"]["contact_name"] = wf["customer"]["name"]
        session["profile"]["business_name"] = wf["customer"]["business_name"]
        session["profile"]["mobile"] = wf["customer"]["mobile"]

    # 2. Sync requirements from GUI into session identified_needs
    reqs = wf.get("discovery", {}).get("requirements", [])
    needs = session.setdefault("identified_needs", [])
    req_to_needs = {
        "broadband_speed": ["speed", "connectivity", "fiber", "high_speed_broadband"],
        "upi_failover": ["payment_redundancy", "upi_pos", "pos_failover"],
        "cctv_security": ["security", "cctv", "surveillance"],
        "static_ip": ["static_ip", "fixed_ip"],
        "whatsapp_api": ["messaging", "whatsapp"],
        "soundbox": ["soundbox", "audio_payment"]
    }
    for r in reqs:
        for need_tag in req_to_needs.get(r, [r]):
            if need_tag not in needs:
                needs.append(need_tag)

    # 3. Synchronize quote with SHARED_QUOTES
    existing_qid = next((qid for qid, q in SHARED_QUOTES.items() if q.get("session_id") == session_id), None)
    rec = wf.get("recommendation", {})
    b_id = rec.get("bundle_id") or f"bundle_{cat}"
    base_bundle = ALL_PACKAGES_MASTER.get(b_id, HERO_BUNDLES_MASTER.get(b_id, HERO_BUNDLES_MASTER["bundle_kirana"]))
    active_addons = rec.get("active_addons", [])
    
    if existing_qid:
        quote_obj = SHARED_QUOTES[existing_qid]
        quote_obj["bundle_id"] = b_id
        quote_obj["bundle_name"] = base_bundle.get("name", rec.get("bundle_name", "Airtel Business Solution"))
        quote_obj["monthly_base_inr"] = base_bundle.get("monthly_inr", rec.get("monthly_base", 1999))
        quote_obj["selected_addons"] = active_addons
    else:
        qid = f"QTE-2026-{str(uuid.uuid4())[:4].upper()}"
        initial_pricing = calculate_quote_pricing(base_bundle["id"], active_addons)
        quote_obj = {
            "quote_id": qid,
            "version_number": 1,
            "session_id": session_id,
            "selected_product_id": base_bundle["id"],
            "bundle_id": base_bundle["id"],
            "bundle_name": base_bundle.get("name", rec.get("bundle_name", "Airtel Business Solution")),
            "monthly_base_inr": base_bundle.get("monthly_inr", rec.get("monthly_base", 1999)),
            "addons": [MODULAR_ADDONS[a] for a in active_addons if a in MODULAR_ADDONS],
            "selected_addons": active_addons,
            "pricing": initial_pricing["pricing"],
            "applicable_gst_rate": 0.18,
            "contract_months": 12,
            "installation_sla_days": 2,
            "created_at": datetime.now().strftime("%d-%b-%Y %H:%M IST"),
            "status": "generated"
        }
        SHARED_QUOTES[qid] = quote_obj

    return session


@app.route("/api/workflow/transition", methods=["POST"])
def api_workflow_transition():
    """Applies a structured transition to the workflow state from GUI or Chat."""
    data = request.json or {}
    session_id = data.get("session_id")
    action = data.get("action")
    payload = data.get("payload", {})
    wf = transition_workflow(session_id, action, payload)
    sync_workflow_to_session(session_id)
    return jsonify({"status": "success", "workflow": wf})
'''

transition_route_target = """@app.route("/api/workflow/transition", methods=["POST"])

def api_workflow_transition():

    \"\"\"Applies a structured transition to the workflow state from GUI or Chat.\"\"\"

    data = request.json or {}

    session_id = data.get("session_id")

    action = data.get("action")

    payload = data.get("payload", {})

    wf = transition_workflow(session_id, action, payload)

    return jsonify({"status": "success", "workflow": wf})"""

assert transition_route_target in text, "transition_route_target not found in app.py"
text = text.replace(transition_route_target, sync_helper_code, 1)

# 4. Add mock LLM endpoint and update advisor_chat
# Find start of advisor_chat
chat_start = text.find('@app.route("/api/advisor/chat", methods=["POST"])')
assert chat_start != -1, "advisor_chat route not found in app.py"

# Find end of advisor_chat (next route)
# In app.py, let's see what route comes after advisor_chat
next_route_match = re.search(r'\n@app\.route\(', text[chat_start + 50:])
assert next_route_match, "next route after advisor_chat not found"
chat_end = chat_start + 50 + next_route_match.start()

new_advisor_chat_code = '''@app.route("/api/advisor/test_mock_llm", methods=["POST"])
def api_test_mock_llm():
    """Endpoint for automated tests to inject mock LLM responses."""
    data = request.json or {}
    mode = data.get("mode")
    if mode == "reset":
        set_test_mock_llm(None)
        return jsonify({"status": "success", "message": "Mock LLM reset"})
    
    response_payload = data.get("response")
    if response_payload:
        set_test_mock_llm(lambda prompt, user_msg: response_payload)
        return jsonify({"status": "success", "message": "Mock LLM set"})
    
    return jsonify({"status": "error", "message": "Missing response or mode"}), 400


@app.route("/api/advisor/chat", methods=["POST"])
def advisor_chat():
    """
    Authoritative unified conversational endpoint grounded dynamically in
    the current workflow stage, customer profile, visible GUI options, and official catalogue.
    """
    data = request.json or {}
    sid = data.get("session_id") or "sess_default"
    message = data.get("message", "").strip()
    raw_cat = data.get("category") or data.get("profile", {}).get("business_type")
    lang = data.get("language", data.get("profile", {}).get("preferred_language", "en")).lower()

    if message:
        detected_lang = detect_natural_language_switch(message)
        if detected_lang:
            lang = detected_lang

    # 1. Fetch & sync authoritative state
    wf = get_or_create_workflow(sid, language=lang)
    session = get_or_create_session(sid, raw_cat or wf.get("discovery", {}).get("business_type", "kirana"), lang)
    sync_workflow_to_session(sid)
    stage = wf.get("stage", "REQUIREMENTS_COLLECTION")

    # 2. Extract user input & update deterministic profile
    if message:
        detect_billing_and_invoicing_intent(message, session)
        extract_and_update_profile(session, message)

    text_clean = message.strip()
    text_low = text_clean.lower()

    # 3. Universal back navigation
    if any(phrase in text_low for phrase in ["go back", "previous step", "back to previous", "take me back", "pichhe jao", "piche jao", "last step", "pichhe chalo", "piche chalo", "prev step"]) or text_low in ["back", "piche", "pichhe", "previous"]:
        wf = transition_workflow(sid, "PREVIOUS_STAGE")
        sync_workflow_to_session(sid)
        reply = "I've navigated back to the previous step. You can review your options or make changes in the panel on the left."
        return jsonify({
            "status": "success",
            "session_id": sid,
            "reply": reply,
            "workflow": wf,
            "quick_replies": ["Continue", "Review Options"]
        })

    # 4. Direct registration details in chat
    if stage in ["CUSTOMER_SIGNUP", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_LOGIN", "USER_TYPE_SELECTION"]:
        signup_data = extract_signup_details(message)
        if signup_data and (stage == "CUSTOMER_SIGNUP" or any(w in text_low for w in ["new", "register", "create", "signup", "sign up", "sweets", "store", "shop", "kirana", "enterprises", "traders", "retail", "provisions", "solutions"])):
            wf["user_type"] = "customer"
            reg_res = register_customer(signup_data, sid)
            c = reg_res.get("customer", {})
            sync_workflow_to_session(sid)
            reply = (
                f"✨ Auto-filled and registered for {c.get('name')} ({c.get('business_name')}) with mobile {c.get('mobile')}!\\n\\n"
                f"I have automatically filled your details in the registration panel on the left and logged your DPDP Act 2023 consent.\\n\\n"
                f"What type of business digital solutions are you exploring today (Kirana & Retail, Clinic, Multi-Store, or Small Factory)?"
            )
            return jsonify({
                "status": "success",
                "session_id": sid,
                "reply": reply,
                "workflow": wf,
                "quick_replies": ["Kirana & Retail", "Clinic & Office", "Multi-Store Chain", "Small Factory"]
            })

    # 5. Check for active quote operations if quote exists
    existing_qid = next((qid for qid, q in SHARED_QUOTES.items() if q.get("session_id") == sid), None)
    active_quote = SHARED_QUOTES.get(existing_qid) if existing_qid else None

    # Bidirectional Quote Action Interceptor (for "How much is CCTV?", "Add CCTV", etc.)
    if active_quote and (stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"] or session.get("discovery_status") == "complete"):
        quote_action = parse_quote_action_intent(message, session, active_quote, lang)
        if quote_action:
            reply_text = quote_action["reply_text"]
            updated_quote = active_quote
            if quote_action.get("requires_quote_update") and active_quote and existing_qid:
                action_type = quote_action["action"]
                target_key = quote_action["target_key"]
                current_addon_keys = [a.get("addon_key") or a.get("id") for a in active_quote.get("addons", [])]

                if action_type == "add_addon" and target_key:
                    if target_key not in current_addon_keys:
                        current_addon_keys.append(target_key)
                    updated_quote, _ = update_shared_quote(existing_qid, selected_addons=current_addon_keys, action_note=f"Added {target_key} via chat")
                    wf_addon_id = MODULAR_ADDONS.get(target_key, {}).get("id", target_key)
                    if wf_addon_id not in wf["recommendation"]["active_addons"]:
                        wf["recommendation"]["active_addons"].append(wf_addon_id)
                    _recalculate_workflow_quote(wf)

                elif action_type == "remove_addon" and target_key:
                    current_addon_keys = [k for k in current_addon_keys if k != target_key and MODULAR_ADDONS.get(target_key, {}).get("id") != k]
                    updated_quote, _ = update_shared_quote(existing_qid, selected_addons=current_addon_keys, action_note=f"Removed {target_key} via chat")
                    wf_addon_id = MODULAR_ADDONS.get(target_key, {}).get("id", target_key)
                    if wf_addon_id in wf["recommendation"]["active_addons"]:
                        wf["recommendation"]["active_addons"].remove(wf_addon_id)
                    _recalculate_workflow_quote(wf)

                elif action_type == "switch_package" and target_key:
                    updated_quote, _ = update_shared_quote(existing_qid, base_bundle_id=target_key, action_note=f"Switched package to {target_key} via chat")
                    wf["recommendation"]["bundle_id"] = target_key
                    _recalculate_workflow_quote(wf)

            wf["messages"].append({
                "sender": "bot",
                "text": reply_text,
                "quick_replies": quote_action.get("quick_replies", [])
            })

            return jsonify({
                "status": "success",
                "session_id": sid,
                "quote_id": existing_qid,
                "reply": reply_text,
                "workflow": wf,
                "profile": session["profile"],
                "identified_needs": session["identified_needs"],
                "discovery_status": "complete",
                "quote": updated_quote,
                "quick_replies": quote_action.get("quick_replies", []),
                "pricing": updated_quote.get("pricing") if updated_quote else None
            })

    # 6. Handle Quote Confirmation & Progression
    if stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
        confirm_phrases = [
            "ok", "okay", "move on", "move ahead", "proceed", "continue", "next", "go ahead",
            "confirm", "book", "take this", "i want this", "buy", "order", "finalize",
            "looks good", "looks fine", "seems ok", "seems good", "all good", "all ok", "all set",
            "sounds good", "sounds great", "fine", "great", "perfect", "done", "deal", "agree",
            "start kyc", "kyc", "verify", "documents", "forward", "let's go", "lets go",
            "theek hai", "thik hai", "sahi hai", "chalo", "aage badho", "aage chalo", "aage"
        ]
        if any(k in text_low for k in confirm_phrases) or any(w in text_low.split() for w in ["ok", "k", "kk", "yes", "haan", "ha", "done", "fine"]):
            transition_workflow(sid, "GO_TO_STAGE", {"stage": "KYC_VERIFICATION"})
            sync_workflow_to_session(sid)
            reply = f"Quotation confirmed for {wf['recommendation']['bundle_name']} at ₹{wf['recommendation']['total_monthly']}/mo! Switched to Smart KYC on the left panel."
            quick = ["Upload GST Certificate", "Upload Udyam MSME Certificate", "Upload Address Proof", "Upload Signatory ID"]
            wf["messages"].append({
                "sender": "bot",
                "text": reply,
                "quick_replies": quick
            })
            return jsonify({
                "status": "success",
                "session_id": sid,
                "quote_id": existing_qid,
                "reply": reply,
                "workflow": wf,
                "quote": active_quote,
                "quick_replies": quick,
                "discovery_status": "complete"
            })

    # 7. Check if deterministic proactive sales discovery has pending steps for billing inquiry
    if session.get("billing_intent", {}).get("active"):
        msg_count = len(session.get("messages", [])) + 1
        is_complete = check_discovery_completion(session["profile"], session["identified_needs"], msg_count, message, session)
        fb_text, fb_quick, fb_bundle, fb_complete, fb_why = generate_deterministic_consultant_reply(session, message, lang)
        if not (is_complete or fb_complete):
            if fb_text:
                if not wf["messages"] or wf["messages"][-1].get("text") != fb_text:
                    wf["messages"].append({"sender": "bot", "text": fb_text, "quick_replies": fb_quick or []})
            return jsonify({
                "workflow": wf,
                "status": "success",
                "session_id": sid,
                "quote_id": None,
                "reply": fb_text,
                "profile": session["profile"],
                "identified_needs": session["identified_needs"],
                "discovery_status": "in_progress",
                "bundle": None,
                "recommendation": None,
                "quote": None,
                "discovery_complete": False,
                "quick_replies": fb_quick,
                "engine": "Airtel Proactive Sales Advisor"
            })

    # 8. Dynamic Grounding: Visible GUI Options & Catalogue
    visible_options = get_visible_gui_options(wf)
    eligible_catalogue = get_eligible_catalogue_options(wf)

    # 9. Model Interpretation with Contextual Fallback
    interpretation = interpret_user_intent_with_context(
        workflow=wf,
        session=session,
        user_message=message,
        language=lang,
        visible_options=visible_options,
        eligible_catalogue=eligible_catalogue,
        live_caller=call_live_llm
    )

    # 10. Strict Backend Validation of Proposed State Changes
    valid_option_ids = {opt["id"] for opt in visible_options}
    valid_catalogue_ids = {item["id"] for item in eligible_catalogue}
    all_valid_ids = valid_option_ids | valid_catalogue_ids | {
        "broadband_speed", "upi_failover", "cctv_security", "static_ip", "whatsapp_api", "soundbox",
        "bundle_kirana", "bundle_clinic", "bundle_multisite", "bundle_manufacturer",
        "P01", "P04", "P07", "P09", "P11", "P15", "P17", "P19", "P22", "P23", "prod_p19_pos",
        "kirana", "clinic", "multisite", "manufacturer"
    }

    target_pids = interpretation.get("target_product_ids", [])
    target_aids = interpretation.get("target_addon_ids", [])
    state_changes = interpretation.get("state_changes", {})

    # Rejection of invalid IDs (e.g. "P99", "FAKE_ID")
    sanitized_pids = [pid for pid in target_pids if pid in all_valid_ids]
    sanitized_aids = [aid for aid in target_aids if aid in all_valid_ids]

    # Apply validated state changes
    reqs = wf.get("discovery", {}).get("requirements", [])
    needs = session.setdefault("identified_needs", [])

    for pid in sanitized_pids:
        if pid in ["broadband_speed", "upi_failover", "cctv_security", "static_ip", "whatsapp_api", "soundbox"]:
            if pid not in reqs:
                reqs.append(pid)
            if pid == "broadband_speed":
                if "speed" not in needs: needs.append("speed")
                if "connectivity" not in needs: needs.append("connectivity")
            elif pid == "cctv_security":
                if "cctv" not in needs: needs.append("cctv")
                if "P23" not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append("P23")
            elif pid == "static_ip":
                if "static_ip" not in needs: needs.append("static_ip")
                if "P11" not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append("P11")
            elif pid == "whatsapp_api":
                if "whatsapp" not in needs: needs.append("whatsapp")
                if "P15" not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append("P15")
            elif pid == "upi_failover":
                if "payment_redundancy" not in needs: needs.append("payment_redundancy")

    for aid in sanitized_aids:
        if aid in MODULAR_ADDONS or aid.startswith("P"):
            if aid not in wf["recommendation"]["active_addons"]:
                wf["recommendation"]["active_addons"].append(aid)

    if "stage" in state_changes and state_changes["stage"] in STAGES:
        wf["stage"] = state_changes["stage"]

    _recalculate_workflow_quote(wf)
    sync_workflow_to_session(sid)

    # Append user and bot messages to workflow
    if message and (not wf["messages"] or wf["messages"][-1].get("text") != message):
        wf["messages"].append({"sender": "user", "text": message})

    bot_reply = interpretation.get("reply", "")
    bot_qr = interpretation.get("quick_replies", [])
    clean_qr = []
    for q in bot_qr:
        if isinstance(q, str) and q.strip() and q.strip() not in ["undefined", "null"]:
            clean_qr.append(q.strip())
        elif isinstance(q, dict) and (q.get("label") or q.get("title")):
            clean_qr.append(q)

    wf["messages"].append({
        "sender": "bot",
        "text": bot_reply,
        "quick_replies": clean_qr
    })

    b_id = wf.get("recommendation", {}).get("bundle_id", "bundle_kirana")
    bundle_data = HERO_BUNDLES_MASTER.get(b_id, HERO_BUNDLES_MASTER["bundle_kirana"])
    existing_qid = next((qid for qid, q in SHARED_QUOTES.items() if q.get("session_id") == sid), None)
    active_quote = SHARED_QUOTES.get(existing_qid) if existing_qid else None

    return jsonify({
        "status": "success",
        "session_id": sid,
        "reply": bot_reply,
        "quick_replies": clean_qr,
        "interpretation": interpretation,
        "workflow": wf,
        "quote": active_quote,
        "quote_id": existing_qid,
        "bundle": bundle_data,
        "profile": session["profile"],
        "identified_needs": session["identified_needs"],
        "discovery_status": "complete" if wf.get("stage") in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "KYC_VERIFICATION", "INSTALLATION_TRACKING"] else "in_progress",
        "engine": "Airtel Unified AI Advisor & Contextual Engine"
    })
'''

text = text[:chat_start] + new_advisor_chat_code + text[chat_end:]

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated app.py with unified advisor_chat, sync_workflow_to_session, and test_mock_llm successfully")
