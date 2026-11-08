with open(r'prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    # Progression from requirements to plan / recommendation
    if stage == "REQUIREMENTS_COLLECTION" and (any(k in text for k in ["done", "show plan", "view plan", "proceed", "continue", "next", "plans", "recommend", "quote", "pricing", "bill", "cost", "how much", "charges", "ready", "move on", "move ahead", "looks good", "all set", "all good", "fine", "theek hai", "chalo", "aage", "send", "go", "forward", "generate", "bundle"]) or any(w in text.split() for w in ["ok", "okay", "k"])):
        transition_workflow(session_id, "GO_TO_STAGE", {"stage": "PLAN_EXPLORATION"})
        return f"Here is your recommended package: {wf['recommendation']['bundle_name']} at ₹{wf['recommendation']['total_monthly']}/mo. You can review the itemized breakdown on the GUI or proceed to KYC."'''

replacement = '''    # Progression from requirements to plan / recommendation
    if stage == "REQUIREMENTS_COLLECTION":
        if any(k in text for k in ["quote", "bill", "monthly bill", "pricing", "charges", "cost"]) and not any(w in text for w in ["billing system", "billing software", "billing machine"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
            return f"Here is your single transparent bill: ₹{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."
        elif any(k in text for k in ["done", "show plan", "view plan", "proceed", "continue", "next", "plans", "recommend", "how much", "ready", "move on", "move ahead", "looks good", "all set", "all good", "fine", "theek hai", "chalo", "aage", "send", "go", "forward", "generate", "bundle"]) or any(w in text.split() for w in ["ok", "okay", "k"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "PLAN_EXPLORATION"})
            return f"Here is your recommended package: {wf['recommendation']['bundle_name']} at ₹{wf['recommendation']['total_monthly']}/mo. You can review the itemized breakdown on the GUI or proceed to KYC."'''

assert target in text, "target not found in customer_workflow_engine.py"
text = text.replace(target, replacement, 1)

with open(r'prototype/customer_workflow_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated stage transition in customer_workflow_engine.py successfully")
