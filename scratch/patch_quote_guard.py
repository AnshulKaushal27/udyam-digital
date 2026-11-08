with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    # Bidirectional Quote Action Interceptor (for "How much is CCTV?", "Add CCTV", "Remove CCTV", "Make it cheaper", etc.)
    if active_quote:
        quote_action = parse_quote_action_intent(message, session, active_quote, lang)'''

replacement = '''    # Bidirectional Quote Action Interceptor (for "How much is CCTV?", "Add CCTV", "Remove CCTV", "Make it cheaper", etc.)
    # Only active when in quote stages or after discovery completion, never during initial requirements collection!
    if active_quote and (stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"] or session.get("discovery_status") == "complete") and stage not in ["REQUIREMENTS_COLLECTION", "BUSINESS_IDENTIFICATION"]:
        quote_action = parse_quote_action_intent(message, session, active_quote, lang)'''

assert target in text, "Target not found in app.py"
text = text.replace(target, replacement, 1)

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated quote action guard in app.py successfully")
