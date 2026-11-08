file_path = "e:/Airtel/prototype/customer_workflow_engine.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update _recalculate_workflow_quote
recalc_start = content.find("def _recalculate_workflow_quote(wf):")
recalc_end = content.find("def get_visible_gui_options", recalc_start)

recalc_code = '''def _recalculate_workflow_quote(wf):
    """Authoritative recalculation of quotation, itemized line items, GST, and setup fees."""
    rec = wf.setdefault("recommendation", {})
    bundle_id = rec.get("bundle_id") or "bundle_kirana"
    bundle = ALL_PACKAGES_MASTER.get(bundle_id) or HERO_BUNDLES_MASTER.get(bundle_id, HERO_BUNDLES_MASTER["bundle_kirana"])

    active_addons = list(rec.get("active_addons", []))

    pricing_data = calculate_quote_pricing(bundle_id, active_addons)
    p = pricing_data["pricing"]

    rec["bundle_id"] = bundle["id"]
    rec["bundle_name"] = bundle["name"]
    rec["monthly_base"] = p["monthly_base_inr"]
    rec["setup_fee"] = p["one_time_setup_inr"]
    rec["contract_months"] = pricing_data.get("contract_months", 12)
    rec["monthly_subtotal"] = p["monthly_subtotal_inr"]
    rec["gst_rate"] = 0.18
    rec["gst_18"] = p["gst_18_inr"]
    rec["total_monthly"] = p["final_monthly_payable_inr"]
    rec["first_payment_total"] = p["first_payment_inr"]
    rec["selected_addons"] = pricing_data.get("selected_addons", [])
    rec["line_items"] = pricing_data.get("line_items", [])
    rec["included_products"] = pricing_data.get("included_products", [])


'''
content = content[:recalc_start] + recalc_code + content[recalc_end:]

# 2. Update ADD_REQUIREMENT, REMOVE_REQUIREMENT, TOGGLE_REQUIREMENT in transition_workflow
act_start = content.find('elif action == "ADD_REQUIREMENT":')
act_end = content.find('elif action == "SELECT_PLAN":', act_start)

actions_code = '''elif action == "ADD_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            display_name = REQ_DISPLAY_NAMES.get(req, req.replace('_', ' ').title())
            pid = REQ_TO_PRODUCT_MAP.get(req)
            b_id = wf.get("recommendation", {}).get("bundle_id", "bundle_kirana")
            b_obj = ALL_PACKAGES_MASTER.get(b_id) or HERO_BUNDLES_MASTER.get(b_id, HERO_BUNDLES_MASTER["bundle_kirana"])
            inc_pids = {p["id"] for p in b_obj.get("products", [])}

            if req not in reqs:
                reqs.append(req)
                if pid and pid not in inc_pids and pid not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append(pid)
                _recalculate_workflow_quote(wf)
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Added requirement: {display_name}.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })
            else:
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Requirement {display_name} is already selected in your configuration.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })

    elif action == "REMOVE_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            display_name = REQ_DISPLAY_NAMES.get(req, req.replace('_', ' ').title())
            pid = REQ_TO_PRODUCT_MAP.get(req)

            if req in reqs:
                reqs.remove(req)
                if pid and pid in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].remove(pid)
                _recalculate_workflow_quote(wf)
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Removed requirement: {display_name}.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })
            else:
                wf["messages"].append({
                    "sender": "bot",
                    "text": f"Requirement {display_name} was not in your selected list.",
                    "quick_replies": [
                        {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                        {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                    ]
                })

    elif action == "TOGGLE_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            display_name = REQ_DISPLAY_NAMES.get(req, req.replace('_', ' ').title())
            pid = REQ_TO_PRODUCT_MAP.get(req)
            b_id = wf.get("recommendation", {}).get("bundle_id", "bundle_kirana")
            b_obj = ALL_PACKAGES_MASTER.get(b_id) or HERO_BUNDLES_MASTER.get(b_id, HERO_BUNDLES_MASTER["bundle_kirana"])
            inc_pids = {p["id"] for p in b_obj.get("products", [])}

            if req in reqs:
                reqs.remove(req)
                ack = f"Removed requirement: {display_name}."
                if pid and pid in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].remove(pid)
            else:
                reqs.append(req)
                ack = f"Added requirement: {display_name}."
                if pid and pid not in inc_pids and pid not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append(pid)
            _recalculate_workflow_quote(wf)
            wf["messages"].append({
                "sender": "bot",
                "text": ack,
                "quick_replies": [
                    {"label": "Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                    {"label": "Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                ]
            })

    '''
content = content[:act_start] + actions_code + content[act_end:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated customer_workflow_engine.py cleanly!")
