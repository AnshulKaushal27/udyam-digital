with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'def sync_workflow_to_session(session_id: str):'

update_shared_quote_code = '''def update_shared_quote(quote_id: str, base_bundle_id: str = None, selected_addons: list = None, action_note: str = ""):
    """Updates quote in SHARED_QUOTES atomically, recomputes pricing, increments version, and logs events."""
    if quote_id not in SHARED_QUOTES:
        return None, None
    q = SHARED_QUOTES[quote_id]
    
    if base_bundle_id:
        bundle_obj = ALL_PACKAGES_MASTER.get(base_bundle_id) or HERO_BUNDLES_MASTER.get(base_bundle_id, HERO_BUNDLES_MASTER["bundle_kirana"])
        q["bundle_id"] = bundle_obj["id"]
        q["bundle_name"] = bundle_obj["name"]
        q["monthly_base_inr"] = bundle_obj["monthly_inr"]
        q["selected_product_id"] = bundle_obj["id"]
        
    current_b_id = q["bundle_id"]
    if selected_addons is not None:
        addon_keys = []
        addon_objs = []
        for a in selected_addons:
            mod = MODULAR_ADDONS.get(a)
            if not mod:
                mod = next((v for v in MODULAR_ADDONS.values() if v.get("id") == a or v.get("addon_key") == a), None)
            if mod:
                if mod["id"] not in addon_keys:
                    addon_keys.append(mod["id"])
                    addon_objs.append(mod)
            else:
                if a not in addon_keys:
                    addon_keys.append(a)
        q["addons"] = addon_objs
        q["selected_addons"] = addon_keys
    else:
        addon_keys = [a.get("addon_key") or a.get("id") for a in q.get("addons", [])]
        
    pricing = calculate_quote_pricing(current_b_id, addon_keys)
    q["pricing"] = pricing["pricing"]
    q["version_number"] = q.get("version_number", 1) + 1
    q["updated_at"] = datetime.now().strftime("%d-%b-%Y %H:%M IST")
    q["status"] = "modified"
    
    mod_hist = q.setdefault("modification_history", [])
    mod_hist.append({
        "version": q["version_number"],
        "timestamp": datetime.now().isoformat(),
        "action": action_note or "Quote updated",
        "bundle_id": q["bundle_id"],
        "addons": addon_keys,
        "total_monthly": pricing["pricing"]["final_monthly_payable_inr"]
    })
    
    QUOTE_EVENTS.append({
        "event_id": f"EVT-{str(uuid.uuid4())[:6].upper()}",
        "event_type": "quote_modified",
        "quote_id": quote_id,
        "version_number": q["version_number"],
        "note": action_note,
        "timestamp": datetime.now().isoformat()
    })
    
    return q, pricing


def sync_workflow_to_session(session_id: str):'''

assert target in text, "sync_workflow_to_session target not found"
text = text.replace(target, update_shared_quote_code, 1)

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added update_shared_quote to app.py successfully")
