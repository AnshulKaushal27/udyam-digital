with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'if active_quote and (stage in ["PLAN_EXPLORATION", "QUOTE_REVIEW", "PACKAGE_CUSTOMIZATION"] or session.get("discovery_status") == "complete") and stage not in ["REQUIREMENTS_COLLECTION", "BUSINESS_IDENTIFICATION"]:'
replacement = 'if active_quote:'

assert target in text, "Target not found in app.py"
text = text.replace(target, replacement, 1)

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated app.py active_quote guard successfully")
