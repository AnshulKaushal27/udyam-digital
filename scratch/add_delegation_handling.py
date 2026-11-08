with open(r'prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '    # 1. Check for inquiries about available additions / options'

delegation_code = '''    # 0. Check for delegation / recommendation request (e.g. "you decide", "what is best", "what do you recommend", "aap decide karo")
    is_delegation = any(k in text_low for k in ["you decide", "what is best", "best for my", "recommend", "aap batao", "tum batao", "suggest", "which plan", "confused", "dont know", "don't know", "what should i choose"])
    if is_delegation:
        reply = "I recommend our Kirana Digital Starter with plug-and-play AirFiber and automatic 4G backup SIM. It is our most popular option engineered to ensure zero payment dropouts."
        return {
            "intent": "select_product",
            "interpreted_need": "Customer delegated package selection to advisor",
            "target_product_ids": ["broadband_speed", "upi_failover"],
            "target_addon_ids": [],
            "state_changes": {"selected_requirements": ["broadband_speed", "upi_failover"]},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": reply,
            "quick_replies": ["View Package Details", "View Available Add-ons", "Confirm Quote"]
        }

    # 1. Check for inquiries about available additions / options'''

assert target in text, "Target not found in conversational_ai.py"
text = text.replace(target, delegation_code, 1)

with open(r'prototype/conversational_ai.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated conversational_ai.py with delegation handling successfully")
