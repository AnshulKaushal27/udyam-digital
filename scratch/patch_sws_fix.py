# Patch sync_workflow_to_session in app.py
with open("e:/Airtel/prototype/app.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '''    if existing_qid:
        quote_obj = SHARED_QUOTES[existing_qid]
        quote_obj["bundle_id"] = b_id
        quote_obj["bundle_name"] = base_bundle.get("name", rec.get("bundle_name", "Airtel Business Solution"))
        quote_obj["monthly_base_inr"] = base_bundle.get("monthly_inr", rec.get("monthly_base", 1999))
        quote_obj["selected_addons"] = active_addons'''

replacement = '''    if existing_qid:
        quote_obj = SHARED_QUOTES[existing_qid]
        quote_obj["bundle_id"] = b_id
        quote_obj["bundle_name"] = base_bundle.get("name", rec.get("bundle_name", "Airtel Business Solution"))
        quote_obj["monthly_base_inr"] = base_bundle.get("monthly_inr", rec.get("monthly_base", 1999))
        quote_obj["selected_addons"] = active_addons
        quote_obj["addons"] = [
            v for k, v in MODULAR_ADDONS.items()
            if k in active_addons or v["id"] in active_addons
        ]
        quote_pricing = calculate_quote_pricing(base_bundle["id"], active_addons)
        quote_obj["pricing"] = quote_pricing["pricing"]
        quote_obj["line_items"] = quote_pricing.get("line_items", [])'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open("e:/Airtel/prototype/app.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated app.py sync_workflow_to_session successfully!")
else:
    print("Target not found in app.py!")
