with open(r'prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '    if any(k in text for k in ["quote", "pricing", "bill", "cost", "how much", "charges"]):\n        transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})'

replacement = '    if any(k in text for k in ["quote", "pricing", "bill", "cost", "how much", "charges"]):\n        if not any(item in text for item in ["cctv", "camera", "cameras", "ip", "static", "whatsapp", "sim", "backup", "pos", "router", "fiber", "speed"]):\n            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})'

if target in text:
    text = text.replace(target, replacement, 1)
    with open(r'prototype/customer_workflow_engine.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully patched price guard in customer_workflow_engine.py")
else:
    print("Target already patched or not found")
