import re

# 1. Update conversational_ai.py
cai_path = "e:/Airtel/prototype/conversational_ai.py"
with open(cai_path, "r", encoding="utf-8") as f:
    cai_text = f.read()

# Update remove_addon in parse_quote_action_intent
old_rem = '''    # 3. Remove Add-on Intent
    is_remove = any(k in text_low for k in ["remove", "hata", "cancel", "don't need", "dont need", "nahi chahiye", "drop", "delete"])
    if is_remove:
        if any(k in text_low for k in ["cctv", "camera"]):'''

new_rem = '''    # 3. Remove Add-on Intent
    is_remove = any(k in text_low for k in ["remove", "hata", "cancel", "don't need", "dont need", "nahi chahiye", "drop", "delete"])
    if is_remove:
        active_addons_in_quote = [a.get("addon_key") or a.get("id") for a in current_quote.get("addons", [])] if current_quote else []
        if any(k in text_low for k in ["cctv", "camera"]):
            if not ("addon_cctv" in active_addons_in_quote or "P23" in active_addons_in_quote):
                return {
                    "action": "remove_addon",
                    "target_key": "addon_cctv",
                    "reply_text": "Cloud CCTV is not currently selected in your configuration. Your current quotation remains unchanged.",
                    "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                    "requires_quote_update": False
                }'''

if old_rem in cai_text:
    cai_text = cai_text.replace(old_rem, new_rem, 1)

# Also for static ip:
old_static = '''        if any(k in text_low for k in ["static ip", "fixed ip"]):
            reply = "I have removed Static Public IP from your quote. Your pricing has been updated."'''

new_static = '''        if any(k in text_low for k in ["static ip", "fixed ip"]):
            if not ("addon_static_ip" in active_addons_in_quote or "P11" in active_addons_in_quote):
                return {
                    "action": "remove_addon",
                    "target_key": "addon_static_ip",
                    "reply_text": "Fixed Static IP Address is not currently selected in your configuration. Your current quotation remains unchanged.",
                    "quick_replies": ["Accept Quote & Verify", "Customize Package", "Itemized Quote"],
                    "requires_quote_update": False
                }
            reply = "I have removed Static Public IP from your quote. Your pricing has been updated."'''

if old_static in cai_text:
    cai_text = cai_text.replace(old_static, new_static, 1)

with open(cai_path, "w", encoding="utf-8") as f:
    f.write(cai_text)
print("Updated conversational_ai.py successfully!")

# 2. Update app.py
app_path = "e:/Airtel/prototype/app.py"
with open(app_path, "r", encoding="utf-8") as f:
    app_text = f.read()

old_app_block = '''                elif action_type == "remove_addon" and target_key:
                    current_addon_keys = [k for k in current_addon_keys if k != target_key and MODULAR_ADDONS.get(target_key, {}).get("id") != k]
                    updated_quote, _ = update_shared_quote(existing_qid, selected_addons=current_addon_keys, action_note=f"Removed {target_key} via chat")
                    wf_addon_id = MODULAR_ADDONS.get(target_key, {}).get("id", target_key)
                    if wf_addon_id in wf["recommendation"]["active_addons"]:
                        wf["recommendation"]["active_addons"].remove(wf_addon_id)
                    _recalculate_workflow_quote(wf)'''

new_app_block = '''                elif action_type == "remove_addon" and target_key:
                    current_addon_keys = [k for k in current_addon_keys if k != target_key and MODULAR_ADDONS.get(target_key, {}).get("id") != k]
                    updated_quote, _ = update_shared_quote(existing_qid, selected_addons=current_addon_keys, action_note=f"Removed {target_key} via chat")
                    wf_addon_id = MODULAR_ADDONS.get(target_key, {}).get("id", target_key)
                    if wf_addon_id in wf["recommendation"]["active_addons"]:
                        wf["recommendation"]["active_addons"].remove(wf_addon_id)
                    matching_req = next((r for r, pid in REQ_TO_PRODUCT_MAP.items() if pid == wf_addon_id), None)
                    if matching_req and matching_req in wf.get("discovery", {}).get("requirements", []):
                        wf["discovery"]["requirements"].remove(matching_req)
                    _recalculate_workflow_quote(wf)'''

if old_app_block in app_text:
    app_text = app_text.replace(old_app_block, new_app_block, 1)

# Also for add_addon:
old_app_add = '''                if action_type == "add_addon" and target_key:
                    if target_key not in current_addon_keys:
                        current_addon_keys.append(target_key)
                    updated_quote, _ = update_shared_quote(existing_qid, selected_addons=current_addon_keys, action_note=f"Added {target_key} via chat")
                    wf_addon_id = MODULAR_ADDONS.get(target_key, {}).get("id", target_key)
                    if wf_addon_id not in wf["recommendation"]["active_addons"]:
                        wf["recommendation"]["active_addons"].append(wf_addon_id)
                    _recalculate_workflow_quote(wf)'''

new_app_add = '''                if action_type == "add_addon" and target_key:
                    if target_key not in current_addon_keys:
                        current_addon_keys.append(target_key)
                    updated_quote, _ = update_shared_quote(existing_qid, selected_addons=current_addon_keys, action_note=f"Added {target_key} via chat")
                    wf_addon_id = MODULAR_ADDONS.get(target_key, {}).get("id", target_key)
                    if wf_addon_id not in wf["recommendation"]["active_addons"]:
                        wf["recommendation"]["active_addons"].append(wf_addon_id)
                    matching_req = next((r for r, pid in REQ_TO_PRODUCT_MAP.items() if pid == wf_addon_id), None)
                    if matching_req and matching_req not in wf.get("discovery", {}).get("requirements", []):
                        wf["discovery"]["requirements"].append(matching_req)
                    _recalculate_workflow_quote(wf)'''

if old_app_add in app_text:
    app_text = app_text.replace(old_app_add, new_app_add, 1)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_text)
print("Updated app.py successfully!")
