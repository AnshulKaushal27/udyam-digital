import re

with open("prototype/conversational_ai.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update generate_deterministic_consultant_reply to avoid hijacking when user stated internet speed or asked about additions
old_kirana_block = '''    else: # Kirana / Micro
        has_payment_mentioned = any(k in text_low for k in ["upi", "pos", "qr", "cash", "payment", "card", "swipe", "scanner", "gpay", "phonepe", "paytm"])
        if has_payment_mentioned or msg_count > 2:
            target_bundle = "prod_p19_pos"
            if "cash" in text_low and not any(k in text_low for k in ["upi", "pos", "qr"]):
                reply = "Understood! For cash-centric retail, our high-speed Fiber ensures your store accounting and billing stay uninterrupted."
            else:
                reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI QR and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."
        if msg_count <= 2:
            if lang == "hi":
                reply = "नमस्ते! आपकी दुकान पर UPI पेमेंट्स और POS मशीन का उपयोग होता है?"
                quick = ["हाँ, UPI और POS दोनों", "सिर्फ QR कोड", "कैश मुख्य रूप से"]
            elif lang == "pa":
                reply = "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਕੀ ਤੁਹਾਡੀ ਦੁਕਾਨ 'ਤੇ UPI ਅਤੇ POS ਮਸ਼ੀਨ ਵਰਤੀ ਜਾਂਦੀ ਹੈ?"
                quick = ["ਹਾਂ, ਦੋਵੇਂ ਵਰਤੇ ਜਾਂਦੇ ਹਨ", "ਸਿਰਫ਼ QR ਕੋਡ", "ਸਿਰਫ਼ ਕੈਸ਼"]
            elif lang == "hinglish":
                reply = "Samajh gaya. Aapki dukaan par UPI payments aur POS machine use karte hain?"
                quick = ["Yes, both UPI & POS", "Only QR payments", "Cash mainly"]
            else:
                reply = "Understood! Does your shop rely heavily on UPI QR payments or card swipe POS machines?"
                quick = ["Yes, both UPI & POS", "Only QR payments", "Cash mainly"]
            return reply, quick, None, False, ""
        else:
            target_bundle = "prod_p19_pos"
            reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."'''

new_kirana_block = '''    else: # Kirana / Micro
        # 1. Check if user asked about connectivity speed or fast internet
        is_speed_need = any(k in text_low for k in ["tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi", "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber", "fibre", "symmetrical", "buffering", "speed chahiye"])
        if is_speed_need:
            if lang == "hi":
                reply = "समझ गया! मैंने आपके लिए High-Speed Symmetrical Fiber विकल्प चुन लिया है ताकि आपको हाई-स्पीड और बफरिंग-फ्री इंटरनेट मिले। इसके अलावा क्या आपको CCTV या Static IP की आवश्यकता है?"
                quick = ["24/7 Cloud CCTV जोड़ें", "Static IP जोड़ें", "डिजिटल बंडल तैयार करें"]
            elif lang == "pa":
                reply = "ਸਮਝ ਗਿਆ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ High-Speed Symmetrical Fiber ਚੁਣ ਲਿਆ ਹੈ ਤਾਂ ਜੋ ਤੁਹਾਨੂੰ ਤੇਜ਼ ਅਤੇ ਬਿਨਾਂ ਰੁਕਾਵਟ ਇੰਟਰਨੈੱਟ ਮਿਲੇ। ਕੀ ਤੁਹਾਨੂੰ CCTV ਜਾਂ Static IP ਦੀ ਲੋੜ ਹੈ?"
                quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ", "Static IP ਸ਼ਾਮਲ ਕਰੋ", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
            elif lang == "hinglish":
                reply = "Samajh gaya! Maine aapke liye High-Speed Symmetrical Fiber select kar diya hai taaki aapko high speed aur zero buffering connectivity mile. Iske alawa kya aapko CCTV surveillance ya Static IP ki zaroorat hai?"
                quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
            else:
                reply = "Understood! I have selected High-Speed Symmetrical Fiber for your setup to ensure consistent high-speed bandwidth with zero buffering. Would you also like to explore Cloud CCTV or Static IP?"
                quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
            return reply, quick, "bundle_kirana", False, "High-speed symmetrical broadband selected for zero-buffering operations."

        # 2. Check if user asked what additions or options are available
        is_additions_query = any(k in text_low for k in ["aur kya", "what else", "additions", "available options", "kya kya add", "other options", "kya kya options", "what additions", "available additions", "add-ons available", "add ons available", "kya add kar sakte"])
        if is_additions_query:
            if lang == "hi":
                reply = "आपके सेटअप के लिए ये अतिरिक्त विकल्प उपलब्ध हैं:\\n1. 24/7 Cloud CCTV (2 कैमरे, 30 दिन रिकॉर्डिंग) - ₹800/माह\\n2. Fixed Static IP Address (सर्वर या NVR के लिए) - ₹300/माह\\n3. Instant UPI & POS Failover (4G बैकअप सिम) - ₹499/माह\\n4. WhatsApp Business API (कस्टमर मैसेजिंग) - ₹999/माह\\nक्या आप इनमें से कोई जोड़ना चाहते हैं?"
                quick = ["Cloud CCTV जोड़ें (+₹800)", "Static IP जोड़ें (+₹300)", "डिजिटल बंडल तैयार करें"]
            elif lang == "pa":
                reply = "ਤੁਹਾਡੇ ਸੈੱਟਅੱਪ ਲਈ ਇਹ ਹੋਰ ਵਿਕਲਪ ਉਪਲਬਧ ਹਨ:\\n1. 24/7 Cloud CCTV (2 ਕੈਮਰੇ) - ₹800/ਮਹੀਨਾ\\n2. Fixed Static IP Address - ₹300/ਮਹੀਨਾ\\n3. Instant UPI Failover (4G ਬੈਕਅੱਪ) - ₹499/ਮਹੀਨਾ\\n4. WhatsApp Business API - ₹999/ਮਹੀਨਾ"
                quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ (+₹800)", "Static IP ਸ਼ਾਮਲ ਕਰੋ (+₹300)", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
            elif lang == "hinglish":
                reply = "Aapke setup ke liye ye catalogue-backed additions available hain:\\n1. 24/7 Cloud CCTV (2 HD Cameras with 30-day cloud recording) - ₹800/mo\\n2. Fixed Static IP Address (for servers or local NVR) - ₹300/mo\\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\\n4. WhatsApp Business API (automated customer updates) - ₹999/mo\\nAap inme se kaunsa option add karna chahte hain?"
                quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
            else:
                reply = "Here are the eligible catalogue-backed additions available for your business:\\n1. 24/7 Cloud CCTV (2 HD Cameras, 30-day cloud recording) - ₹800/mo\\n2. Fixed Static IP Address - ₹300/mo\\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\\n4. WhatsApp Business API - ₹999/mo\\nWould you like to add any of these to your setup?"
                quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
            return reply, quick, None, False, "Listing catalogue-backed eligible additions."

        # 3. Check for specific payment mentions
        has_payment_mentioned = any(k in text_low for k in ["upi", "pos", "qr", "cash", "payment", "card", "swipe", "scanner", "gpay", "phonepe", "paytm"])
        if has_payment_mentioned or msg_count > 2:
            target_bundle = "prod_p19_pos"
            if "cash" in text_low and not any(k in text_low for k in ["upi", "pos", "qr"]):
                reply = "Understood! For cash-centric retail, our high-speed Fiber ensures your store accounting and billing stay uninterrupted."
            else:
                reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI QR and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."
        if msg_count <= 2:
            if lang == "hi":
                reply = "नमस्ते! आपकी दुकान पर UPI पेमेंट्स और POS मशीन का उपयोग होता है?"
                quick = ["हाँ, UPI और POS दोनों", "सिर्फ QR कोड", "कैश मुख्य रूप से"]
            elif lang == "pa":
                reply = "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਕੀ ਤੁਹਾਡੀ ਦੁਕਾਨ 'ਤੇ UPI ਅਤੇ POS ਮਸ਼ੀਨ ਵਰਤੀ ਜਾਂਦੀ ਹੈ?"
                quick = ["ਹਾਂ, ਦੋਵੇਂ ਵਰਤੇ ਜਾਂਦੇ ਹਨ", "ਸਿਰਫ਼ QR ਕੋਡ", "ਸਿਰਫ਼ ਕੈਸ਼"]
            elif lang == "hinglish":
                reply = "Samajh gaya. Aapki dukaan par UPI payments aur POS machine use karte hain?"
                quick = ["Yes, both UPI & POS", "Only QR payments", "Cash mainly"]
            else:
                reply = "Understood! Does your shop rely heavily on UPI QR payments or card swipe POS machines?"
                quick = ["Yes, both UPI & POS", "Only QR payments", "Cash mainly"]
            return reply, quick, None, False, ""
        else:
            target_bundle = "prod_p19_pos"
            reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."'''

assert old_kirana_block in content, "old_kirana_block not found"
content = content.replace(old_kirana_block, new_kirana_block, 1)

# 2. Append the new unified interpretation functions at the end of conversational_ai.py
extension_code = '''

# -------------------------------------------------------------------------
# 11. UNIFIED CONTEXTUAL PROMPT & STRUCTURED INTERPRETATION ENGINE
# -------------------------------------------------------------------------
_GLOBAL_TEST_MOCK_LLM = None

def set_test_mock_llm(mock_fn):
    """Test hook to register a mock LLM function for deterministic integration testing."""
    global _GLOBAL_TEST_MOCK_LLM
    _GLOBAL_TEST_MOCK_LLM = mock_fn

def build_unified_advisor_prompt(
    workflow: Dict[str, Any],
    session: Dict[str, Any],
    user_message: str,
    language: str,
    visible_options: List[Dict[str, Any]],
    eligible_catalogue: List[Dict[str, Any]]
) -> str:
    """
    Constructs a comprehensive system prompt grounding the model in:
    - Current workflow stage
    - Profile and identified needs
    - Numbered GUI options currently visible to the customer
    - Eligible catalogue products & add-ons with pricing
    - Conversation history
    - Structured JSON output format
    """
    stage = workflow.get("stage", "REQUIREMENTS_COLLECTION")
    profile = session.get("profile", {})
    btype = workflow.get("discovery", {}).get("business_type", profile.get("business_type", "kirana"))
    reqs = workflow.get("discovery", {}).get("requirements", [])
    rec = workflow.get("recommendation", {})
    cur_bundle = rec.get("bundle_id", "bundle_kirana")
    active_addons = rec.get("active_addons", [])
    
    # Format visible options for the prompt with clear 1-based indices
    options_summary = []
    for opt in visible_options:
        idx = opt.get("index")
        name = opt.get("name")
        oid = opt.get("id")
        desc = opt.get("description", "")
        sel = "[SELECTED]" if opt.get("selected") else "[UNSELECTED]"
        price = f" ({opt.get('price_inr')}/mo)" if "price_inr" in opt else ""
        options_summary.append(f"  Option {idx}: ID='{oid}' | Name='{name}'{price} | Status={sel} | Desc: {desc}")
    visible_str = "\\n".join(options_summary) if options_summary else "  (None currently displayed)"

    # Format catalogue options
    cat_summary = []
    for item in eligible_catalogue:
        cid = item.get("id")
        cname = item.get("name")
        cprice = item.get("price")
        cdesc = item.get("description")
        cat_summary.append(f"  Item {cid}: '{cname}' | Price={cprice} | {cdesc}")
    catalogue_str = "\\n".join(cat_summary)

    prompt = (
        "You are the Airtel Business GenAI Digital Advisor for 'Project Udyam Digital' (Bharti Airtel SYNC 2026 Innovation Challenge).\\n"
        "Your role is to understand MSME business owners' needs and recommend appropriate Airtel Business solutions.\\n\\n"
        f"CURRENT WORKFLOW STAGE: {stage}\\n"
        f"CUSTOMER PROFILE: Business Type='{btype}', Known Info={json.dumps(profile, ensure_ascii=False)}\\n"
        f"CURRENT SELECTIONS: Requirements={json.dumps(reqs)}, Bundle='{cur_bundle}', Active Add-ons={json.dumps(active_addons)}\\n\\n"
        "CURRENTLY VISIBLE GUI OPTIONS ON CUSTOMER SCREEN (Ordered 1 to N):\\n"
        f"{visible_str}\\n\\n"
        "ELIGIBLE AIRTEL PRODUCT CATALOGUE (Official items & pricing):\\n"
        f"{catalogue_str}\\n\\n"
        f"PREFERRED LANGUAGE: {language} (Respond in English, Hindi Devanagari, Punjabi Gurmukhi, or conversational Hinglish based on user input).\\n\\n"
        "INTERPRETATION & CONVERSATIONAL RULES:\\n"
        "1. INTERPRET MEANING over literal phrase matching. Do not rely on brittle word matches.\\n"
        "   - 'mujhe tez internet chahiye', 'need faster Wi-Fi', 'internet slow hai', 'high speed connection chahiye' -> interpret as a connectivity speed need.\\n"
        "     In REQUIREMENTS_COLLECTION, map this to visible Option 'broadband_speed' (High-Speed Symmetrical Fiber) and mark it for selection.\\n"
        "   - 'aur kya kya additions available hain', 'what else is available', 'what add-ons can I get' -> interpret as 'list_available_options'.\\n"
        "     Explain the visible/eligible catalogue additions (e.g. Cloud CCTV, Static IP, WhatsApp API, Cloud POS Billing, UPI failover) with names and pricing.\\n"
        "     DO NOT continue asking unrelated payment/POS questions when the customer asked what is available!\\n"
        "   - References like 'the second option', 'option 2', 'dusra option' MUST be resolved against the currently visible numbered options list above.\\n"
        "2. GROUNDED REPLIES: Never invent non-existent products, fake discounts, or unverified prices. Keep pricing strictly grounded in the catalogue.\\n"
        "3. SINGLE CONVERSATIONAL FOCUS: Do not repeat questions already answered. If the customer just expressed a need or asked a question, address it directly.\\n"
        "4. OUTPUT FORMAT: You MUST return ONLY a valid JSON object matching the exact schema below:\\n"
        "{\\n"
        '  "intent": "select_product | add_need | list_available_options | ask_question | provide_information | change_profile | confirm | other",\\n'
        '  "interpreted_need": "short plain-language description of customer need",\\n'
        '  "target_product_ids": ["catalogue or GUI option ID, e.g. broadband_speed, P23, etc."],\\n'
        '  "target_addon_ids": ["catalogue-backed addon ID if applicable, e.g. P23, P11"],\\n'
        '  "state_changes": {\\n'
        '    "selected_requirements": ["broadband_speed"],\\n'
        '    "bundle_id": null,\\n'
        '    "selected_addons": []\\n'
        '  },\\n'
        '  "needs_clarification": false,\\n'
        '  "clarification_question": null,\\n'
        '  "reply": "<friendly, professional natural language response in requested language>",\\n'
        '  "quick_replies": ["option 1", "option 2"]\\n'
        "}\\n"
        "Output ONLY the JSON object. Do not wrap in extra markdown or commentary."
    )
    return prompt

def interpret_user_intent_fallback(
    workflow: Dict[str, Any],
    session: Dict[str, Any],
    user_message: str,
    language: str,
    visible_options: List[Dict[str, Any]],
    eligible_catalogue: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Deterministic contextual fallback when live LLM is unreachable or returns invalid format.
    Grounded strictly in visible GUI options and catalogue.
    """
    text_clean = user_message.strip()
    text_low = text_clean.lower()
    stage = workflow.get("stage", "REQUIREMENTS_COLLECTION")
    reqs = list(workflow.get("discovery", {}).get("requirements", []))
    
    # 1. Check for inquiries about available additions / options
    is_additions_query = any(k in text_low for k in [
        "aur kya", "what else", "additions", "available options", "kya kya add",
        "other options", "kya kya options", "what additions", "available additions",
        "add-ons available", "add ons available", "kya add kar sakte", "available items"
    ])
    if is_additions_query:
        if language == "hi":
            reply = "आपके सेटअप के लिए ये अतिरिक्त विकल्प उपलब्ध हैं:\\n1. 24/7 Cloud CCTV (2 कैमरे, 30 दिन रिकॉर्डिंग) - ₹800/माह\\n2. Fixed Static IP Address (सर्वर या NVR के लिए) - ₹300/माह\\n3. Instant UPI & POS Failover (4G बैकअप सिम) - ₹499/माह\\n4. WhatsApp Business API (कस्टमर मैसेजिंग) - ₹999/माह\\nक्या आप इनमें से कोई जोड़ना चाहते हैं?"
            quick = ["Cloud CCTV जोड़ें (+₹800)", "Static IP जोड़ें (+₹300)", "डिजिटल बंडल तैयार करें"]
        elif language == "pa":
            reply = "ਤੁਹਾਡੇ ਸੈੱਟਅੱਪ ਲਈ ਇਹ ਹੋਰ ਵਿਕਲਪ ਉਪਲਬਧ ਹਨ:\\n1. 24/7 Cloud CCTV (2 ਕੈਮਰੇ) - ₹800/ਮਹੀਨਾ\\n2. Fixed Static IP Address - ₹300/ਮਹੀਨਾ\\n3. Instant UPI Failover (4G ਬੈਕਅੱਪ) - ₹499/ਮਹੀਨਾ\\n4. WhatsApp Business API - ₹999/ਮਹੀਨਾ"
            quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ (+₹800)", "Static IP ਸ਼ਾਮਲ ਕਰੋ (+₹300)", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
        elif language == "hinglish":
            reply = "Aapke setup ke liye ye catalogue-backed additions available hain:\\n1. 24/7 Cloud CCTV (2 HD Cameras with 30-day cloud recording) - ₹800/mo\\n2. Fixed Static IP Address (for servers or local NVR) - ₹300/mo\\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\\n4. WhatsApp Business API (automated customer updates) - ₹999/mo\\nAap inme se kaunsa option add karna chahte hain?"
            quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
        else:
            reply = "Here are the eligible catalogue-backed additions available for your business:\\n1. 24/7 Cloud CCTV (2 HD Cameras, 30-day cloud recording) - ₹800/mo\\n2. Fixed Static IP Address - ₹300/mo\\n3. Instant UPI & POS Failover (automatic 4G backup SIM) - ₹499/mo\\n4. WhatsApp Business API - ₹999/mo\\nWould you like to add any of these to your setup?"
            quick = ["Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)", "Add WhatsApp API (+₹999)", "Generate Digital Bundle"]
            
        return {
            "intent": "list_available_options",
            "interpreted_need": "Customer inquired about available additions and add-ons",
            "target_product_ids": [],
            "target_addon_ids": [],
            "state_changes": {},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": quick
        }

    # 2. Check for Ordinal Reference (e.g. 'the second option', 'option 2', 'dusra option')
    ordinal_map = {
        "first": 1, "1st": 1, "pehla": 1, "option 1": 1,
        "second": 2, "2nd": 2, "dusra": 2, "option 2": 2,
        "third": 3, "3rd": 3, "teesra": 3, "option 3": 3,
        "fourth": 4, "4th": 4, "chautha": 4, "option 4": 4
    }
    target_idx = None
    for k, idx in ordinal_map.items():
        if k in text_low:
            target_idx = idx
            break
            
    if target_idx and visible_options and target_idx <= len(visible_options):
        selected_opt = visible_options[target_idx - 1]
        opt_id = selected_opt.get("id")
        opt_name = selected_opt.get("name")
        opt_type = selected_opt.get("type")
        
        reply = f"I have selected {opt_name} for you based on option {target_idx} from the screen."
        state_changes = {}
        target_pids = [opt_id]
        target_aids = []
        
        if opt_type == "requirement":
            state_changes["selected_requirements"] = [opt_id]
        elif opt_type == "addon":
            state_changes["selected_addons"] = [opt_id]
            target_aids = [opt_id]
        elif opt_type == "base_plan":
            state_changes["bundle_id"] = opt_id
            
        return {
            "intent": "select_product",
            "interpreted_need": f"Selected option {target_idx}: {opt_name}",
            "target_product_ids": target_pids,
            "target_addon_ids": target_aids,
            "state_changes": state_changes,
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
        }

    # 3. Check for Fast Internet / Broadband Speed / Fiber Need
    is_speed_need = any(k in text_low for k in [
        "tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi",
        "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber",
        "fibre", "symmetrical", "buffering", "speed chahiye"
    ])
    if is_speed_need:
        if language == "hi":
            reply = "समझ गया! मैंने आपके लिए High-Speed Symmetrical Fiber विकल्प चुन लिया है ताकि आपको हाई-स्पीड और बफरिंग-फ्री इंटरनेट मिले। इसके अलावा क्या आपको CCTV या Static IP की आवश्यकता है?"
            quick = ["24/7 Cloud CCTV जोड़ें", "Static IP जोड़ें", "डिजिटल बंडल तैयार करें"]
        elif language == "pa":
            reply = "ਸਮਝ ਗਿਆ! ਮੈਂ ਤੁਹਾਡੇ ਲਈ High-Speed Symmetrical Fiber ਚੁਣ ਲਿਆ ਹੈ ਤਾਂ ਜੋ ਤੁਹਾਨੂੰ ਤੇਜ਼ ਅਤੇ ਬਿਨਾਂ ਰੁਕਾਵਟ ਇੰਟਰਨੈੱਟ ਮਿਲੇ। ਕੀ ਤੁਹਾਨੂੰ CCTV ਜਾਂ Static IP ਦੀ ਲੋੜ ਹੈ?"
            quick = ["Cloud CCTV ਸ਼ਾਮਲ ਕਰੋ", "Static IP ਸ਼ਾਮਲ ਕਰੋ", "ਪੈਕੇਜ ਤਿਆਰ ਕਰੋ"]
        elif language == "hinglish":
            reply = "Samajh gaya! Maine aapke liye High-Speed Symmetrical Fiber select kar diya hai taaki aapko high speed aur zero buffering connectivity mile. Iske alawa kya aapko CCTV surveillance ya Static IP ki zaroorat hai?"
            quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
        else:
            reply = "Understood! I have selected High-Speed Symmetrical Fiber for your setup to ensure consistent high-speed bandwidth with zero buffering. Would you also like to explore Cloud CCTV or Static IP?"
            quick = ["View Available Add-ons", "Generate Digital Bundle", "Add 24/7 Cloud CCTV"]
            
        return {
            "intent": "add_need",
            "interpreted_need": "High-speed symmetrical internet connectivity",
            "target_product_ids": ["broadband_speed"],
            "target_addon_ids": [],
            "state_changes": {"selected_requirements": ["broadband_speed"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": quick
        }

    # 4. Check for CCTV / Cloud Surveillance
    is_cctv_need = any(k in text_low for k in ["cctv", "camera", "cameras", "surveillance", "security camera"])
    if is_cctv_need:
        return {
            "intent": "add_need",
            "interpreted_need": "24/7 Cloud CCTV camera security",
            "target_product_ids": ["cctv_security"],
            "target_addon_ids": ["P23"],
            "state_changes": {"selected_requirements": ["cctv_security"], "selected_addons": ["P23"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": "Added 24/7 Cloud CCTV Surveillance (+₹800/mo) with 2 HD cameras and 30-day cloud recording.",
            "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
        }

    # 5. Check for Static IP
    is_static_ip = any(k in text_low for k in ["static ip", "fixed ip", "public ip", "server", "nvr"])
    if is_static_ip:
        return {
            "intent": "add_need",
            "interpreted_need": "Fixed static public IP address",
            "target_product_ids": ["static_ip"],
            "target_addon_ids": ["P11"],
            "state_changes": {"selected_requirements": ["static_ip"], "selected_addons": ["P11"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": "Added Fixed Static IP Address (+₹300/mo) for your dedicated servers and secure remote access.",
            "quick_replies": ["View Available Add-ons", "Generate Digital Bundle", "Confirm Quote"]
        }

    # 6. Check for UPI / POS failover
    is_upi_need = any(k in text_low for k in ["upi", "pos failover", "payment fail", "qr code", "card swipe", "soundbox"])
    if is_upi_need:
        return {
            "intent": "add_need",
            "interpreted_need": "Instant UPI & POS failover connectivity",
            "target_product_ids": ["upi_failover"],
            "target_addon_ids": ["P09"],
            "state_changes": {"selected_requirements": ["upi_failover"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": "Selected Instant UPI & POS Failover to guarantee zero transaction dropouts during peak rush.",
            "quick_replies": ["High-Speed Symmetrical Fiber", "24/7 Cloud CCTV", "Generate Digital Bundle"]
        }

    # 7. Check for Confirm / Progression
    is_confirm = any(k in text_low for k in ["proceed", "move on", "continue", "next", "confirm", "generate", "start kyc", "looks good", "theek hai", "chalo", "done", "okay"])
    if is_confirm:
        next_stage = "PLAN_EXPLORATION" if stage == "REQUIREMENTS_COLLECTION" else "KYC_VERIFICATION"
        return {
            "intent": "confirm",
            "interpreted_need": f"Proceed to next stage ({next_stage})",
            "target_product_ids": [],
            "target_addon_ids": [],
            "state_changes": {"stage": next_stage},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": f"Proceeding to {next_stage.replace('_', ' ').title()}. Your selections have been saved.",
            "quick_replies": ["Continue", "Review Selections"]
        }

    # Default fallback: helpful, stage-aware, non-hijacking
    if stage == "REQUIREMENTS_COLLECTION":
        default_reply = "Could you tell me more about your setup? You can select any of the visible options on the left (High-Speed Fiber, CCTV, Static IP, UPI failover) or describe your needs here."
        default_qr = ["High-Speed Fiber", "24/7 Cloud CCTV", "Fixed Static IP", "Instant UPI Failover"]
    else:
        default_reply = "I am here to help you configure the right Airtel Business plan. You can ask about available add-ons, customize your quote, or proceed to Smart KYC."
        default_qr = ["View Available Add-ons", "Confirm Quote & KYC", "Compare Other Plans"]
        
    return {
        "intent": "ask_question",
        "interpreted_need": "General customer inquiry",
        "target_product_ids": [],
        "target_addon_ids": [],
        "state_changes": {},
        "needs_clarification": False,
        "clarification_question": None,
        "reply": default_reply,
        "quick_replies": default_qr
    }

def interpret_user_intent_with_context(
    workflow: Dict[str, Any],
    session: Dict[str, Any],
    user_message: str,
    language: str,
    visible_options: List[Dict[str, Any]],
    eligible_catalogue: List[Dict[str, Any]],
    mock_fn=None,
    live_caller=None
) -> Dict[str, Any]:
    """
    Interprets customer turn using the configured LLM path (or mock), grounded dynamically in visible options and catalogue.
    Falls back gracefully to deterministic contextual fallback if LLM is unavailable or fails.
    """
    global _GLOBAL_TEST_MOCK_LLM
    active_mock = mock_fn or _GLOBAL_TEST_MOCK_LLM
    prompt = build_unified_advisor_prompt(workflow, session, user_message, language, visible_options, eligible_catalogue)
    
    # 1. If test mock is active, call mock function
    if active_mock:
        try:
            mock_res = active_mock(prompt, user_message)
            if isinstance(mock_res, dict):
                return mock_res
            if isinstance(mock_res, str):
                clean_json = mock_res.strip().replace("```json", "").replace("```", "")
                return json.loads(clean_json)
        except Exception:
            pass

    # 2. Try live LLM caller if provided or available
    if live_caller:
        try:
            raw_text, bundle_id, engine = live_caller(prompt, user_message)
            if raw_text:
                clean_json = raw_text.strip().replace("```json", "").replace("```", "")
                parsed = json.loads(clean_json)
                if isinstance(parsed, dict) and "reply" in parsed:
                    return parsed
        except Exception:
            pass

    # 3. Deterministic Contextual Fallback
    return interpret_user_intent_fallback(workflow, session, user_message, language, visible_options, eligible_catalogue)
'''

content = content + extension_code

with open("prototype/conversational_ai.py", "w", encoding="utf-8") as f:
    f.write(content)

print("conversational_ai.py successfully updated with unified contextual interpretation.")
