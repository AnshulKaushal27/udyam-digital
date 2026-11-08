"""Update advisor_chat fallback in app.py"""
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''    # High quality fallback
    if lang == "hi":
        reply = f"नमस्ते! आपके व्यवसाय के लिए '{best_bundle['name']}' सबसे उपयुक्त है। इसमें ₹{best_bundle['monthly_inr']}/माह में तेज़ इंटरनेट, बैकअप और डिजिटल टूल्स मिलते हैं।"
    elif lang == "hinglish":
        reply = f"Namaste ji! Aapke business ke liye best package hai '{best_bundle['name']}'. ₹{best_bundle['monthly_inr']}/month me continuous internet aur backup tools milenge."
    else:
        reply = f"Based on your requirements, we recommend '{best_bundle['name']}' at ₹{best_bundle['monthly_inr']}/month with 99.9% uptime SLA."

    return jsonify({
        "status": "success",
        "session_id": session["session_id"],
        "quote_id": quote_id,
        "reply": reply,
        "profile": profile,
        "identified_needs": session["identified_needs"],
        "discovery_status": profile["discovery_status"],
        "bundle": best_bundle,
        "recommendation": rec_result,
        "quote": quote_obj,
        "discovery_complete": is_complete,
        "quick_replies": ["Looks good", "Check Price", "Can I add Wi-Fi?"],
        "engine": "Airtel Rule Engine"
    })'''

replacement = '''    # Proactive Sales Consultant Fallback
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

content_clean = content.replace('\r\n', '\n')
target_clean = target.replace('\r\n', '\n')
replacement_clean = replacement.replace('\r\n', '\n')

assert target_clean in content_clean, 'Target not found in content'
content_clean = content_clean.replace(target_clean, replacement_clean, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(content_clean)

print("advisor_chat fallback updated successfully!")
