"""Apply model switch to qwen/qwen3.8-27b, max_tokens, contextual quick replies, and anti-loop guardrails."""
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add sanitize_assistant_reply and get_contextual_quick_replies helper
helpers = '''def sanitize_assistant_reply(text):
    """Guards against LLM repetition loops and chained questions."""
    if not text:
        return ""
    # If the response contains runaway repeated questions, keep only the first coherent question
    if "?" in text:
        parts = text.split("?")
        if len(parts) > 2:
            return parts[0].strip() + "?"
    return text.strip()

def get_contextual_quick_replies(session, user_text="", is_finished=False):
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
    return ["1:1 Leased Line", "Static IP for ERP", "Machine IoT sensors"]
'''

old_gen = '''        if grok:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {grok}", "Content-Type": "application/json"}
                payload = {
                    "model": "openai/gpt-oss-120b",
                    "messages": llm_messages,
                    "temperature": 0.3,
                    "stream": True
                }'''

new_gen = '''        if grok:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {grok}", "Content-Type": "application/json"}
                payload = {
                    "model": "qwen/qwen3.8-27b",
                    "messages": llm_messages,
                    "temperature": 0.2,
                    "max_tokens": 150,
                    "stream": True
                }'''

assert old_gen in content, "old_gen not found"
content = content.replace(old_gen, new_gen, 1)

# 2. Add helpers right above advisor_chat_stream
target_def = 'def build_advisor_prompt(session, lang):'
content = content.replace(target_def, helpers + '\n' + target_def, 1)

# 3. Update quick replies fallback in advisor_chat_stream
old_qr_fallback = '''            if not parsed_meta.get("quick_replies"):
                parsed_meta["quick_replies"] = ["1–2 staff", "3–5 staff", "More than 5"]'''

new_qr_fallback = '''            if not parsed_meta.get("quick_replies"):
                parsed_meta["quick_replies"] = get_contextual_quick_replies(session, last_user_text, parsed_meta.get("discovery_complete", False))'''

assert old_qr_fallback in content, "old_qr_fallback not found"
content = content.replace(old_qr_fallback, new_qr_fallback, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("prototype/app.py updated with Qwen model, max_tokens, and contextual quick replies!")
