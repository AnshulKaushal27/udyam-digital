import re

with open("prototype/customer_workflow_engine.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update _recalculate_workflow_quote to include all add-ons and additions
target_calc = '''def _recalculate_workflow_quote(wf):
    """Internal helper to calculate single transparent monthly bill."""
    base = wf["recommendation"]["monthly_base"]
    addons = wf["recommendation"]["active_addons"]
    
    addon_prices = {
        "P15": 999, # WhatsApp API Starter
        "P23": 800, # Cloud CCTV 2 Cameras
        "P11": 300, # Static IP
        "P07": 299  # Business SIM 40GB
    }
    addon_sum = sum(addon_prices.get(a, 0) for a in addons)
    subtotal = base + addon_sum
    gst = round(subtotal * 0.18)
    total = subtotal + gst
    
    wf["recommendation"]["monthly_subtotal"] = subtotal
    wf["recommendation"]["gst_18"] = gst
    wf["recommendation"]["total_monthly"] = total'''

new_calc = '''def _recalculate_workflow_quote(wf):
    """Internal helper to calculate single transparent monthly bill."""
    base = wf["recommendation"]["monthly_base"]
    addons = wf["recommendation"].get("active_addons", [])
    
    addon_prices = {
        "P15": 999,  # WhatsApp API Starter
        "P23": 800,  # Cloud CCTV 2 Cameras
        "P11": 300,  # Static IP
        "P07": 299,  # Business SIM (50GB)
        "P17": 499,  # Additional Cloud Backup (1 TB)
        "P19": 599,  # Cloud POS & GST Billing Counter
        "P04": 899,  # Biz 5G AirFiber 100 Mbps
        "P09": 499,  # Backup 4G/5G Failover
        "P22": 399   # Secure Commercial Wi-Fi
    }
    addon_sum = sum(addon_prices.get(a, 0) for a in addons)
    subtotal = base + addon_sum
    gst = round(subtotal * 0.18)
    total = subtotal + gst
    
    wf["recommendation"]["monthly_subtotal"] = subtotal
    wf["recommendation"]["gst_18"] = gst
    wf["recommendation"]["total_monthly"] = total

def get_visible_gui_options(workflow):
    """
    Returns the exact ordered list of options currently displayed on the customer GUI.
    Each item contains stable 1-based index, stable id, display name, type, description, and selected state.
    """
    stage = workflow.get("stage", "USER_TYPE_SELECTION")
    
    if stage == "REQUIREMENTS_COLLECTION":
        reqs = workflow.get("discovery", {}).get("requirements", [])
        return [
            {
                "index": 1,
                "id": "upi_failover",
                "name": "Instant UPI & POS Failover",
                "type": "requirement",
                "description": "Guaranteed backup SIM so customer payments never drop during evening rush.",
                "selected": "upi_failover" in reqs,
                "linked_addon_id": "P09"
            },
            {
                "index": 2,
                "id": "broadband_speed",
                "name": "High-Speed Symmetrical Fiber",
                "type": "requirement",
                "description": "Consistent upload and download bandwidth with zero buffering.",
                "selected": "broadband_speed" in reqs,
                "linked_product_id": "P01"
            },
            {
                "index": 3,
                "id": "cctv_security",
                "name": "24/7 Cloud CCTV Surveillance",
                "type": "requirement",
                "description": "Remote store monitoring with 30-day encrypted cloud recording.",
                "selected": "cctv_security" in reqs,
                "linked_addon_id": "P23",
                "price_inr": 800
            },
            {
                "index": 4,
                "id": "static_ip",
                "name": "Fixed Static IP Address",
                "type": "requirement",
                "description": "Host local servers, biometric attendance, or remote CCTV securely.",
                "selected": "static_ip" in reqs,
                "linked_addon_id": "P11",
                "price_inr": 300
            }
        ]
        
    elif stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"]:
        rec = workflow.get("recommendation", {})
        cur_bundle = rec.get("bundle_id", "bundle_kirana")
        active_addons = rec.get("active_addons", [])
        return [
            {"index": 1, "id": "bundle_kirana", "name": "Kirana Digital Starter", "type": "base_plan", "price_inr": 1999, "selected": cur_bundle == "bundle_kirana", "description": "100 Mbps AirFiber + 4G Failover + WhatsApp API"},
            {"index": 2, "id": "bundle_clinic", "name": "Clinic & Professional Office Suite", "type": "base_plan", "price_inr": 3499, "selected": cur_bundle == "bundle_clinic", "description": "300 Mbps Fiber + 1TB Cloud Backup + Google Workspace"},
            {"index": 3, "id": "bundle_multisite", "name": "Multi-Site Retail Pro", "type": "base_plan", "price_inr": 7999, "selected": cur_bundle == "bundle_multisite", "description": "1 Gbps Fiber + SD-WAN Failover + 4x CCTV"},
            {"index": 4, "id": "bundle_manufacturer", "name": "Small Manufacturing Suite", "type": "base_plan", "price_inr": 14999, "selected": cur_bundle == "bundle_manufacturer", "description": "20 Mbps 1:1 Leased Line + Static IP + IoT Telemetry"},
            {"index": 5, "id": "P15", "name": "WhatsApp Business API", "type": "addon", "price_inr": 999, "selected": "P15" in active_addons, "description": "1,000 verified promotional/order update conversations"},
            {"index": 6, "id": "P23", "name": "Cloud CCTV 2 Cameras", "type": "addon", "price_inr": 800, "selected": "P23" in active_addons, "description": "2 HD cameras with 30-day encrypted cloud recording"},
            {"index": 7, "id": "P11", "name": "Fixed Static Public IP Address", "type": "addon", "price_inr": 300, "selected": "P11" in active_addons, "description": "Public IP for local billing servers & NVR access"},
            {"index": 8, "id": "P07", "name": "Business Postpaid SIM (50GB)", "type": "addon", "price_inr": 299, "selected": "P07" in active_addons, "description": "Unlimited voice calls + 50 GB CUG data"},
            {"index": 9, "id": "P17", "name": "Additional Cloud Backup (1 TB)", "type": "addon", "price_inr": 499, "selected": "P17" in active_addons, "description": "AES-256 cloud backup for accounting software & files"},
            {"index": 10, "id": "P19", "name": "Cloud POS & GST Billing Counter", "type": "addon", "price_inr": 599, "selected": "P19" in active_addons, "description": "GST-ready invoicing, barcode scanner, inventory & UPI receipts"}
        ]
        
    elif stage == "BUSINESS_IDENTIFICATION":
        cur_type = workflow.get("discovery", {}).get("business_type", "kirana")
        return [
            {"index": 1, "id": "kirana", "name": "Kirana & Retail Store", "type": "category", "selected": cur_type == "kirana", "description": "AirFiber 5G, UPI Soundbox, Billing POS failover"},
            {"index": 2, "id": "clinic", "name": "Healthcare Clinic & Office", "type": "category", "selected": cur_type == "clinic", "description": "Symmetrical Fiber 300, Cloud Records Backup & Secure Wi-Fi"},
            {"index": 3, "id": "multisite", "name": "Multi-Site Retail Chain", "type": "category", "selected": cur_type == "multisite", "description": "SD-WAN Central Controller, Static IP & Multi-Branch CCTV"},
            {"index": 4, "id": "manufacturer", "name": "Small Factory", "type": "category", "selected": cur_type == "manufacturer", "description": "Dedicated leased line, Static IP & IoT telemetry"}
        ]
        
    return []

def get_eligible_catalogue_options(workflow):
    """
    Returns verified catalogue-backed products and add-ons eligible for the customer.
    """
    return [
        {"id": "P01", "name": "Biz Fibre 100 Mbps", "category": "Connectivity", "price": "₹999/mo", "description": "High-speed symmetrical broadband with zero buffering"},
        {"id": "P02", "name": "Biz Fibre 300 Mbps", "category": "Connectivity", "price": "₹1,499/mo", "description": "Ultra-fast symmetrical fiber for multi-device operations"},
        {"id": "P04", "name": "Biz 5G AirFiber 100 Mbps", "category": "Connectivity", "price": "₹899/mo", "description": "Instant wireless plug-and-play broadband"},
        {"id": "P09", "name": "Backup 4G/5G Failover", "category": "Connectivity", "price": "₹499/mo", "description": "Automatic 4G/5G failover for POS and UPI payment terminals"},
        {"id": "P11", "name": "Fixed Static Public IP Address", "category": "Connectivity", "price": "₹300/mo", "description": "Public IP for local billing servers, remote access & NVR"},
        {"id": "P15", "name": "WhatsApp Business API", "category": "Customer Marketing", "price": "₹999/mo", "description": "1,000 verified promotional and order messaging conversations"},
        {"id": "P17", "name": "Additional Cloud Backup (1 TB)", "category": "Cloud & Storage", "price": "₹499/mo", "description": "Encrypted offsite backup for accounting data and invoices"},
        {"id": "P19", "name": "Cloud POS & GST Billing Counter", "category": "Billing Solutions", "price": "₹599/mo", "description": "GST-ready invoicing, barcode scanner, inventory sync & instant UPI receipts"},
        {"id": "P23", "name": "Cloud CCTV (2 HD Cameras)", "category": "Surveillance & Security", "price": "₹800/mo", "description": "2 HD outdoor/indoor cameras with mobile live view & 30-day cloud recording"}
    ]'''

assert target_calc in content, "target_calc not found"
content = content.replace(target_calc, new_calc, 1)

# 2. Fix friendly requirement names in transition_workflow TOGGLE/ADD/REMOVE
old_req_block = '''    elif action == "ADD_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            if req not in reqs:
                reqs.append(req)
            addon_map = {"cctv_security": "P23", "static_ip": "P11", "whatsapp_api": "P15", "sim_cards": "P07"}
            if req in addon_map and addon_map[req] not in wf["recommendation"]["active_addons"]:
                wf["recommendation"]["active_addons"].append(addon_map[req])
            _recalculate_workflow_quote(wf)
            wf["messages"].append({"sender": "bot", "text": f"Added requirement: {req.replace('_', ' ').title()}."})

    elif action == "REMOVE_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            if req in reqs:
                reqs.remove(req)
            addon_map = {"cctv_security": "P23", "static_ip": "P11", "whatsapp_api": "P15", "sim_cards": "P07"}
            if req in addon_map and addon_map[req] in wf["recommendation"]["active_addons"]:
                wf["recommendation"]["active_addons"].remove(addon_map[req])
            _recalculate_workflow_quote(wf)
            wf["messages"].append({
                "sender": "bot",
                "text": f"Removed requirement: {req.replace('_', ' ').title()}.",
                "quick_replies": [
                    {"label": "🚀 Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                    {"label": "➕ Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                ]
            })

    elif action == "TOGGLE_REQUIREMENT":
        req = payload.get("requirement")
        if req:
            reqs = wf["discovery"]["requirements"]
            if req in reqs:
                reqs.remove(req)
                ack = f"Removed requirement: {req.replace('_', ' ').title()}."
            else:
                reqs.append(req)
                ack = f"Added requirement: {req.replace('_', ' ').title()}."
                # Auto-align addon
                addon_map = {"cctv_security": "P23", "static_ip": "P11", "whatsapp_api": "P15", "sim_cards": "P07"}
                if req in addon_map and addon_map[req] not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append(addon_map[req])
            _recalculate_workflow_quote(wf)
            wf["messages"].append({
                "sender": "bot",
                "text": ack,
                "quick_replies": [
                    {"label": "🚀 Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                    {"label": "➕ Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                ]
            })'''

new_req_block = '''    elif action == "ADD_REQUIREMENT":
        req = payload.get("requirement")
        friendly_names = {
            "broadband_speed": "High-Speed Symmetrical Fiber",
            "upi_failover": "Instant UPI & POS Failover",
            "cctv_security": "24/7 Cloud CCTV Surveillance",
            "static_ip": "Fixed Static IP Address",
            "whatsapp_api": "WhatsApp Business API"
        }
        if req:
            reqs = wf["discovery"]["requirements"]
            if req not in reqs:
                reqs.append(req)
            addon_map = {"cctv_security": "P23", "static_ip": "P11", "whatsapp_api": "P15", "sim_cards": "P07"}
            if req in addon_map and addon_map[req] not in wf["recommendation"]["active_addons"]:
                wf["recommendation"]["active_addons"].append(addon_map[req])
            _recalculate_workflow_quote(wf)
            display_name = friendly_names.get(req, req.replace('_', ' ').title())
            wf["messages"].append({"sender": "bot", "text": f"Added requirement: {display_name}."})

    elif action == "REMOVE_REQUIREMENT":
        req = payload.get("requirement")
        friendly_names = {
            "broadband_speed": "High-Speed Symmetrical Fiber",
            "upi_failover": "Instant UPI & POS Failover",
            "cctv_security": "24/7 Cloud CCTV Surveillance",
            "static_ip": "Fixed Static IP Address",
            "whatsapp_api": "WhatsApp Business API"
        }
        if req:
            reqs = wf["discovery"]["requirements"]
            if req in reqs:
                reqs.remove(req)
            addon_map = {"cctv_security": "P23", "static_ip": "P11", "whatsapp_api": "P15", "sim_cards": "P07"}
            if req in addon_map and addon_map[req] in wf["recommendation"]["active_addons"]:
                wf["recommendation"]["active_addons"].remove(addon_map[req])
            _recalculate_workflow_quote(wf)
            display_name = friendly_names.get(req, req.replace('_', ' ').title())
            wf["messages"].append({
                "sender": "bot",
                "text": f"Removed requirement: {display_name}.",
                "quick_replies": [
                    {"label": "🚀 Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                    {"label": "➕ Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                ]
            })

    elif action == "TOGGLE_REQUIREMENT":
        req = payload.get("requirement")
        friendly_names = {
            "broadband_speed": "High-Speed Symmetrical Fiber",
            "upi_failover": "Instant UPI & POS Failover",
            "cctv_security": "24/7 Cloud CCTV Surveillance",
            "static_ip": "Fixed Static IP Address",
            "whatsapp_api": "WhatsApp Business API"
        }
        if req:
            reqs = wf["discovery"]["requirements"]
            display_name = friendly_names.get(req, req.replace('_', ' ').title())
            if req in reqs:
                reqs.remove(req)
                ack = f"Removed requirement: {display_name}."
                addon_map = {"cctv_security": "P23", "static_ip": "P11", "whatsapp_api": "P15", "sim_cards": "P07"}
                if req in addon_map and addon_map[req] in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].remove(addon_map[req])
            else:
                reqs.append(req)
                ack = f"Added requirement: {display_name}."
                # Auto-align addon
                addon_map = {"cctv_security": "P23", "static_ip": "P11", "whatsapp_api": "P15", "sim_cards": "P07"}
                if req in addon_map and addon_map[req] not in wf["recommendation"]["active_addons"]:
                    wf["recommendation"]["active_addons"].append(addon_map[req])
            _recalculate_workflow_quote(wf)
            wf["messages"].append({
                "sender": "bot",
                "text": ack,
                "quick_replies": [
                    {"label": "🚀 Generate Digital Bundle", "action": "GO_TO_STAGE", "value": "PLAN_EXPLORATION"},
                    {"label": "➕ Add Another Tool", "action": "GO_TO_STAGE", "value": "REQUIREMENTS_COLLECTION"}
                ]
            })'''

assert old_req_block in content, "old_req_block not found"
content = content.replace(old_req_block, new_req_block, 1)

with open("prototype/customer_workflow_engine.py", "w", encoding="utf-8") as f:
    f.write(content)

print("customer_workflow_engine.py successfully updated.")
