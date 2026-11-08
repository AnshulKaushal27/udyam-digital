"""Update prototype/app.py with conversational AI, language synchronization, and indecision handling."""
import re

with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update get_or_create_session
old_session_code = '''        CUSTOMER_SESSIONS[new_sid] = {
            "session_id": new_sid,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "profile": {
                "business_type": btype,
                "business_name": "",
                "employees": None,
                "locations": 1,
                "current_connectivity": "",
                "digital_tools": [],
                "pain_points": [],
                "peak_usage": "",
                "special_requirements": [],
                "budget_min": None,
                "budget_max": None,
                "preferred_language": language,
                "discovery_status": "in_progress" # "in_progress" | "complete"
            },
            "identified_needs": [],
            "messages": []
        }
        return CUSTOMER_SESSIONS[new_sid]
    
    session = CUSTOMER_SESSIONS[sid]
    session["updated_at"] = datetime.now().isoformat()
    if language:
        session["profile"]["preferred_language"] = language'''

new_session_code = '''        CUSTOMER_SESSIONS[new_sid] = {
            "session_id": new_sid,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "profile": {
                "business_type": btype,
                "business_name": "",
                "employees": None,
                "locations": 1,
                "current_connectivity": "",
                "digital_tools": [],
                "pain_points": [],
                "peak_usage": "",
                "special_requirements": [],
                "budget_min": None,
                "budget_max": None,
                "preferred_language": language,
                "discovery_status": "in_progress" # "in_progress" | "complete"
            },
            "identified_needs": [],
            "preference_tracking": {},
            "billing_intent": {
                "active": False,
                "requested_feature": None,
                "current_method": None,
                "gst_required": None,
                "monthly_invoices": None,
                "deployment_preference": None,
                "inventory_needed": None,
                "catalogue_product_id": "P19",
                "catalogue_product_name": "Cloud POS & Billing",
                "catalogue_price_inr": 599
            },
            "recommendation_lifecycle": {
                "status": "not_ready",
                "last_bundle_id": None,
                "rejection_reason": None,
                "alternative_offered": False
            },
            "messages": []
        }
        return CUSTOMER_SESSIONS[new_sid]
    
    session = CUSTOMER_SESSIONS[sid]
    session["updated_at"] = datetime.now().isoformat()
    if language:
        session["profile"]["preferred_language"] = language
    if "preference_tracking" not in session:
        session["preference_tracking"] = {}
    if "billing_intent" not in session:
        session["billing_intent"] = {
            "active": False,
            "requested_feature": None,
            "current_method": None,
            "gst_required": None,
            "monthly_invoices": None,
            "deployment_preference": None,
            "inventory_needed": None,
            "catalogue_product_id": "P19",
            "catalogue_product_name": "Cloud POS & Billing",
            "catalogue_price_inr": 599
        }
    if "recommendation_lifecycle" not in session:
        session["recommendation_lifecycle"] = {
            "status": "not_ready",
            "last_bundle_id": None,
            "rejection_reason": None,
            "alternative_offered": False
        }'''

assert old_session_code in content, "old_session_code not found in content"
content = content.replace(old_session_code, new_session_code, 1)

# 2. Update check_discovery_completion
old_disc = '''def check_discovery_completion(profile, identified_needs, message_count, user_text=""):
    """
    Discovery Completeness Evaluator:
    Determines whether sufficient contextual intelligence has been gathered to make a recommendation.
    Never forces the merchant into a long interrogation.
    """
    text_low = user_text.lower()'''

new_disc = '''def check_discovery_completion(profile, identified_needs, message_count, user_text="", session=None):
    """
    Discovery Completeness Evaluator:
    Determines whether sufficient contextual intelligence has been gathered to make a recommendation.
    Never forces the merchant into a long interrogation.
    """
    text_low = user_text.lower()
    
    # Check if billing/invoicing intent is active
    if session and session.get("billing_intent", {}).get("active"):
        b_intent = session["billing_intent"]
        # Only complete once monthly volume (~300-400) or deployment preference is captured
        if b_intent.get("monthly_invoices") is not None or b_intent.get("deployment_preference") is not None:
            return True
        return False'''

assert old_disc in content, "old_disc not found in content"
content = content.replace(old_disc, new_disc, 1)

# 3. Add Punjabi starters and update lang_key in get_default_conversation_starter
old_starters_end = '''    category_data = starters.get(btype, starters["kirana"])
    lang_key = lang if lang in ["en", "hi", "hinglish"] else "en"'''

new_starters_end = '''    # Add Punjabi variants
    starters["kirana"]["pa"] = {
        "message": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਤੁਹਾਡੀ ਦੁਕਾਨ 'ਤੇ ਲਗਭਗ ਕਿੰਨੇ ਲੋਕ ਜਾਂ ਸਟਾਫ ਕੰਮ ਕਰਦੇ ਹਨ?",
        "quick_replies": ["ਸਿਰਫ਼ ਮੈਂ (1 ਵਿਅਕਤੀ)", "2–3 ਸਟਾਫ", "4–8 ਸਟਾਫ", "8 ਤੋਂ ਵੱਧ"]
    }
    starters["clinic"]["pa"] = {
        "message": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਡਾਕਟਰ ਸਾਹਿਬ! ਕੀ ਮਰੀਜ਼ਾਂ ਦੇ ਰਿਕਾਰਡ ਅਤੇ ਬਿਲਿੰਗ ਲਈ ਕਲਾਊਡ ਬੈਕਅੱਪ ਜਾਂ ਤੇਜ਼ ਇੰਟਰਨੈਟ ਚਾਹੀਦਾ ਹੈ?",
        "quick_replies": ["ਹਾਈ-ਸਪੀਡ ਫਾਈਬਰ Wi-Fi", "ਸੁਰੱਖਿਅਤ 1TB ਕਲਾਊਡ ਬੈਕਅੱਪ", "ਬਿਲਿੰਗ & ਈਮੇਲ ਸੂਟ", "ਇਹ ਸਾਰੇ"]
    }
    starters["multisite"]["pa"] = {
        "message": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਤੁਹਾਡੇ ਕੁੱਲ ਕਿੰਨੇ ਸਟੋਰ ਜਾਂ ਬ੍ਰਾਂਚਾਂ ਹਨ?",
        "quick_replies": ["2–3 ਸਟੋਰ", "4–8 ਸਟੋਰ", "10 ਤੋਂ ਵੱਧ", "ਨਵੀਂ ਬ੍ਰਾਂਚ ਸ਼ੁਰੂ ਕਰ ਰਹੇ ਹਾਂ"]
    }
    starters["manufacturer"]["pa"] = {
        "message": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਕੀ ਤੁਹਾਡੀ ਫੈਕਟਰੀ ਲਈ ERP ਜਾਂ ਮਸ਼ੀਨ IoT ਵਾਸਤੇ ਡੈਡੀਕੇਟਿਡ ਲੀਜ਼ਡ ਲਾਈਨ ਚਾਹੀਦੀ ਹੈ?",
        "quick_replies": ["1:1 ਡੈਡੀਕੇਟਿਡ ਲੀਜ਼ਡ ਲਾਈਨ", "ERP ਲਈ ਸਟੈਟਿਕ IP", "ਮਸ਼ੀਨ IoT ਸੈਂਸਰ", "ਇਹ ਸਾਰੇ"]
    }

    category_data = starters.get(btype, starters["kirana"])
    lang_key = lang if lang in ["en", "hi", "pa", "hinglish"] else "en"'''

assert old_starters_end in content, "old_starters_end not found"
content = content.replace(old_starters_end, new_starters_end, 1)

# 4. Add /api/advisor/session/language endpoint
old_session_reset = '''@app.route("/api/advisor/session/reset", methods=["POST"])
def advisor_reset_session():'''

new_session_reset = '''@app.route("/api/advisor/session/language", methods=["POST"])
def advisor_update_session_language():
    """Dynamically updates language preference in active session without wiping context or history."""
    data = request.json or {}
    sid = data.get("session_id")
    lang = data.get("language", "en").lower()
    if lang not in ["en", "hi", "pa", "hinglish"]:
        lang = "en"
    
    session = CUSTOMER_SESSIONS.get(sid)
    if session:
        session["profile"]["preferred_language"] = lang
        session["updated_at"] = datetime.now().isoformat()
    return jsonify({
        "status": "success",
        "session_id": sid,
        "language": lang
    })

@app.route("/api/advisor/session/reset", methods=["POST"])
def advisor_reset_session():'''

assert old_session_reset in content, "old_session_reset not found"
content = content.replace(old_session_reset, new_session_reset, 1)

# 5. Update build_advisor_prompt
old_build_prompt = '''def build_advisor_prompt(session, lang):
    profile = session["profile"]
    btype = profile.get("business_type", "kirana")
    target_bundle_id = f"bundle_{btype}"
    bundle_info = HERO_BUNDLES.get(target_bundle_id, HERO_BUNDLES["bundle_kirana"])
    identified_needs = session.get("identified_needs", [])
    needs_summary = ", ".join([f"{n['category']} ({n['type']})" for n in identified_needs]) if identified_needs else "None yet"

    return (
        "You are an experienced, empathetic, and consultative Airtel Business sales advisor in India helping an MSME business owner.\\n"
        "Your objective: Understand the merchant's operational reality deeply before recommending a digital bundle.\\n\\n"
        "CORE CONVERSATION PRINCIPLES:\\n"
        "1. ASK EXACTLY ONE QUESTION AT A TIME. Keep normal responses strictly between 5 and 25 words.\\n"
        "2. Acknowledge what the customer just shared with natural empathy (e.g., 'Samajh gaya.', 'Theek hai.', 'Understood.', 'Achha, that makes sense.').\\n"
        "3. DO NOT ASK QUESTIONS ALREADY ANSWERED. Inspect the Known Profile below.\\n"
        "4. DO NOT dump product catalogues, technical specs, or pricing prematurely.\\n"
        "5. Language: Strictly respond in the requested language: " + lang.upper() + " (English, Hindi, or conversational Hinglish). Keep vocabulary natural (kirana shop, billing, staff, UPI, disconnections).\\n"
        "6. Handle edge cases naturally:\\n"
        "   - Ambiguous answers: ask a polite clarifying follow-up.\\n"
        "   - Requirement changes: warmly acknowledge and pivot context.\\n"
        "   - Unrelated questions: answer politely in 10-15 words, then gently resume business discovery.\\n\\n"
        f"TARGET SEGMENT: {btype.upper()} ({bundle_info['segment']})\\n"
        f"KNOWN PROFILE: {json.dumps(profile, ensure_ascii=False)}\\n"
        f"IDENTIFIED NEEDS: {needs_summary}\\n\\n"
        "RECOMMENDATION TRANSITION:\\n"
        "When discovery is complete (or customer asks for a recommendation), transition warmly in 1 short sentence explaining why this Airtel bundle solves their core problem, and set recommend_bundle to '" + target_bundle_id + "'.\\n\\n"
        "STREAMING OUTPUT FORMAT:\\n"
        "Output your conversational message to the user directly (5-25 words).\\n"
        "Then, on a new line, output the exact marker ||META|| followed by a single-line JSON object:\\n"
        '{"profile_updates": {"employees": <number or null>, "locations": <number or null>, "pain_points": [...], "digital_tools": [...]}, '
        '"quick_replies": ["option 1", "option 2", "option 3"], '
        '"recommend_bundle": "' + target_bundle_id + '" or null, '
        '"discovery_complete": true or false, '
        '"why_brief": "<1 sentence plain-language explanation if recommending>"}\\n'
        "Always supply 2 to 4 contextual quick replies that make it effortless for the merchant to answer the current question."
    )'''

new_build_prompt = '''def build_advisor_prompt(session, lang):
    return build_proactive_sales_prompt(session, lang)'''

assert old_build_prompt in content, "old_build_prompt not found"
content = content.replace(old_build_prompt, new_build_prompt, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Part 1 changes applied to app.py successfully!")
