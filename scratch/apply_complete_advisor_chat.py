with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

chat_start = text.find('@app.route("/api/advisor/test_mock_llm", methods=["POST"])')
if chat_start == -1:
    chat_start = text.find('@app.route("/api/advisor/chat", methods=["POST"])')
assert chat_start != -1, "chat start route not found"

next_route_match = text.find('@app.route("/api/quote/customize", methods=["POST"])')
assert next_route_match != -1, "next route /api/quote/customize not found"

complete_chat_code = '''@app.route("/api/advisor/test_mock_llm", methods=["POST"])
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

    # 5. Check active quote & parse bidirectional quote actions
    existing_qid = next((qid for qid, q in SHARED_QUOTES.items() if q.get("session_id") == sid), None)
    active_quote = SHARED_QUOTES.get(existing_qid) if existing_qid else None

    # Bidirectional Quote Action Interceptor (for "How much is CCTV?", "Add CCTV", "Remove CCTV", "Make it cheaper", etc.)
    if active_quote:
        quote_action = parse_quote_action_intent(message, session, active_quote, lang)
        if quote_action:
            reply_text = quote_action["reply_text"]
            updated_quote = active_quote
            if quote_action.get("requires_quote_update") and existing_qid:
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

    # 7. Check if deterministic billing sales discovery workflow is in progress
    if session.get("billing_intent", {}).get("active"):
        msg_count = len(session.get("messages", [])) + 1
        is_complete = check_discovery_completion(session["profile"], session["identified_needs"], msg_count, message, session)
        fb_text, fb_quick, fb_bundle, fb_complete, fb_why = generate_deterministic_consultant_reply(session, message, lang)
        is_finished = is_complete or fb_complete

        if not is_finished:
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
        else:
            # Billing discovery finished! Build and persist the quote
            session["profile"]["discovery_status"] = "complete"
            rec_result = evaluate_bundle_recommendation(session["profile"], session["identified_needs"])
            best_bundle = ALL_PACKAGES_MASTER.get(fb_bundle) if (fb_bundle and fb_bundle in ALL_PACKAGES_MASTER) else rec_result["best_bundle"]
            quote_id = existing_qid or f"QTE-2026-{str(uuid.uuid4())[:4].upper()}"
            initial_pricing = calculate_quote_pricing(best_bundle["id"], [])
            quote_obj = {
                "quote_id": quote_id,
                "version_number": 1,
                "session_id": sid,
                "selected_product_id": best_bundle["id"],
                "bundle_id": best_bundle["id"],
                "bundle_name": best_bundle["name"],
                "segment_display": best_bundle.get("segment_display", best_bundle.get("segment", "Enterprise")),
                "monthly_base_inr": best_bundle["monthly_inr"],
                "addons": [],
                "selected_addons": [],
                "pricing": initial_pricing["pricing"],
                "applicable_gst_rate": 0.18,
                "contract_months": best_bundle.get("contract_months", 12),
                "installation_sla_days": best_bundle.get("lead_time_days", 2),
                "sla": best_bundle.get("sla", "99.5% Uptime"),
                "included_products": best_bundle.get("products", []),
                "match_score": rec_result.get("match_score", 95),
                "dimension_scores": rec_result.get("dimension_scores", {}),
                "matching_reasons": rec_result.get("matching_reasons", []),
                "unmet_requirements": rec_result.get("unmet_requirements", []),
                "compatible_addons": rec_result.get("compatible_addons", []),
                "alternative_bundle": rec_result.get("alternative_bundle"),
                "budget_analysis": rec_result.get("budget_analysis"),
                "created_at": datetime.now().strftime("%d-%b-%Y %H:%M IST"),
                "updated_at": datetime.now().strftime("%d-%b-%Y %H:%M IST"),
                "valid_until": "Valid for 30 Days",
                "status": "generated"
            }
            SHARED_QUOTES[quote_id] = quote_obj
            wf["recommendation"]["bundle_id"] = best_bundle["id"]
            wf["recommendation"]["bundle_name"] = best_bundle["name"]
            wf["recommendation"]["monthly_base"] = best_bundle["monthly_inr"]
            wf["stage"] = "PLAN_EXPLORATION"
            _recalculate_workflow_quote(wf)
            sync_workflow_to_session(sid)

            if fb_text:
                wf["messages"].append({"sender": "bot", "text": fb_text, "quick_replies": fb_quick or []})

            return jsonify({
                "status": "success",
                "session_id": sid,
                "quote_id": quote_id,
                "reply": fb_text,
                "profile": session["profile"],
                "identified_needs": session["identified_needs"],
                "discovery_status": "complete",
                "bundle": best_bundle,
                "recommendation": rec_result,
                "quote": quote_obj,
                "discovery_complete": True,
                "quick_replies": fb_quick,
                "workflow": wf,
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

text = text[:chat_start] + complete_chat_code + text[next_route_match:]

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated app.py with complete advisor_chat successfully")
