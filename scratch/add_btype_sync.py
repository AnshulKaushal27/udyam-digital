with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    if message:
        detect_billing_and_invoicing_intent(message, session)
        extract_and_update_profile(session, message)'''

replacement = '''    if message:
        detect_billing_and_invoicing_intent(message, session)
        extract_and_update_profile(session, message)
        if session["profile"]["business_type"] != wf.get("discovery", {}).get("business_type"):
            new_btype = session["profile"]["business_type"]
            wf["discovery"]["business_type"] = new_btype
            new_b_id = f"bundle_{new_btype}"
            wf["recommendation"]["bundle_id"] = new_b_id
            if new_b_id in HERO_BUNDLES_MASTER:
                wf["recommendation"]["bundle_name"] = HERO_BUNDLES_MASTER[new_b_id]["name"]
                wf["recommendation"]["monthly_base"] = HERO_BUNDLES_MASTER[new_b_id]["monthly_inr"]
            _recalculate_workflow_quote(wf)'''

assert target in text, "Target not found"
text = text.replace(target, replacement, 1)

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated btype sync in app.py successfully")
