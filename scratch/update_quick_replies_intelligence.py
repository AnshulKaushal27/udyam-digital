"""Update detect_billing_and_invoicing_intent and get_contextual_quick_replies."""
with open(r'E:\Airtel\prototype\conversational_ai.py', 'r', encoding='utf-8') as f:
    c_ai = f.read()

# In detect_billing_and_invoicing_intent, ensure paper/manual activates billing_intent
old_meth = '''    # 2. Current Method Extraction
    if any(k in text_low for k in ["paper", "manual", "kacha bill", "haath se", "khata", "diary"]):
        b_intent["current_method"] = "paper"
    elif any(k in text_low for k in ["software", "tally", "busy", "computerized"]):
        b_intent["current_method"] = "software"
    elif any(k in text_low for k in ["excel", "spreadsheet", "sheet"]):
        b_intent["current_method"] = "spreadsheet"'''

new_meth = '''    # 2. Current Method Extraction
    if any(k in text_low for k in ["paper", "manual", "kacha bill", "haath se", "khata", "diary"]):
        b_intent["current_method"] = "paper"
        b_intent["active"] = True
    elif any(k in text_low for k in ["software", "tally", "busy", "computerized"]):
        b_intent["current_method"] = "software"
        b_intent["active"] = True
    elif any(k in text_low for k in ["excel", "spreadsheet", "sheet"]):
        b_intent["current_method"] = "spreadsheet"
        b_intent["active"] = True'''

assert old_meth in c_ai, "old_meth not found in conversational_ai.py"
c_ai = c_ai.replace(old_meth, new_meth, 1)

with open(r'E:\Airtel\prototype\conversational_ai.py', 'w', encoding='utf-8') as f:
    f.write(c_ai)

# In app.py, update get_contextual_quick_replies to inspect bot_text
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

old_get_qr = '''def get_contextual_quick_replies(session, user_text="", is_finished=False):
    """Contextual quick reply pills dynamically matching current conversation stage."""
    b_intent = session.get("billing_intent", {})
    if is_finished:
        return ["View Package Details", "Check Installation SLA", "Request Callback"]
    if b_intent.get("active"):
        if b_intent.get("current_method") is None:
            return ["Paper/manual billing", "Invoicing software", "Simple spreadsheet"]
        elif b_intent.get("gst_required") is None:
            return ["Yes, need GST invoices", "Simple non-GST is fine", "Not sure"]
        elif b_intent.get("monthly_invoices") is None:
            return ["100–200 / month", "300–400 / month", "500+ / month"]
        else:
            return ["Cloud-based billing", "Offline desktop billing", "You decide"]
    btype = session.get("profile", {}).get("business_type", "kirana")
    if btype == "kirana":
        return ["Just me (1 person)", "2–3 staff", "4–8 staff", "More than 8"]
    elif btype == "clinic":
        return ["High-speed Fiber & Wi-Fi", "1TB Cloud Backup", "Billing & Email Suite"]
    elif btype == "multisite":
        return ["2–3 stores", "4–8 stores", "10+ outlets"]
    return ["1:1 Leased Line", "Static IP for ERP", "Machine IoT sensors"]'''

new_get_qr = '''def get_contextual_quick_replies(session, user_text="", is_finished=False, bot_text=""):
    """Contextual quick reply pills dynamically matching current conversation stage."""
    if is_finished:
        return ["View Package Details", "Check Installation SLA", "Request Callback"]
    
    bot_low = bot_text.lower() if bot_text else ""
    user_low = user_text.lower() if user_text else ""
    
    # 1. Match based on what the assistant just asked
    if "gst" in bot_low:
        return ["Yes, need GST invoices", "Simple non-GST is fine", "Not sure"]
    if any(k in bot_low for k in ["how many", "month", "invoices", "volume", "bills"]):
        return ["100–200 / month", "300–400 / month", "500+ / month"]
    if any(k in bot_low for k in ["create and send invoices", "paper", "excel", "software"]):
        return ["Paper/manual", "Excel/spreadsheet", "Invoicing software"]
        
    # 2. Match based on billing intent state
    b_intent = session.get("billing_intent", {})
    if b_intent.get("active"):
        if b_intent.get("current_method") is None:
            return ["Paper/manual", "Invoicing software", "Simple spreadsheet"]
        elif b_intent.get("gst_required") is None:
            return ["Yes, need GST invoices", "Simple non-GST is fine", "Not sure"]
        elif b_intent.get("monthly_invoices") is None:
            return ["100–200 / month", "300–400 / month", "500+ / month"]
        else:
            return ["Cloud-based billing", "Offline desktop billing", "You decide"]
            
    btype = session.get("profile", {}).get("business_type", "kirana")
    if btype == "kirana":
        return ["Just me (1 person)", "2–3 staff", "4–8 staff", "More than 8"]
    elif btype == "clinic":
        return ["High-speed Fiber & Wi-Fi", "1TB Cloud Backup", "Billing & Email Suite"]
    elif btype == "multisite":
        return ["2–3 stores", "4–8 stores", "10+ outlets"]
    return ["1:1 Leased Line", "Static IP for ERP", "Machine IoT sensors"]'''

assert old_get_qr in app_code, "old_get_qr not found in app.py"
app_code = app_code.replace(old_get_qr, new_get_qr, 1)

# In advisor_chat_stream, pass user_part to get_contextual_quick_replies
old_call = 'get_contextual_quick_replies(session, last_user_text, parsed_meta.get("discovery_complete", False))'
new_call = 'get_contextual_quick_replies(session, last_user_text, parsed_meta.get("discovery_complete", False), user_part)'
app_code = app_code.replace(old_call, new_call, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Updated contextual quick replies and billing activation successfully!")
