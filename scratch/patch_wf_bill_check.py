def main():
    path = "prototype/customer_workflow_engine.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    target1 = '''    if stage == "REQUIREMENTS_COLLECTION":
        if any(k in text for k in ["quote", "bill", "monthly bill", "pricing", "charges", "cost"]) and not any(w in text for w in ["billing system", "billing software", "billing machine"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
            return f"Here is your single transparent bill: \u20b9{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."'''

    replacement1 = '''    if stage == "REQUIREMENTS_COLLECTION":
        if (any(k in text for k in ["quote", "monthly bill", "the bill", "pricing", "charges", "cost"]) or any(w in text.split() for w in ["bill", "quote"])) and not any(w in text for w in ["billing", "billing system", "billing software", "billing machine"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
            return f"Here is your single transparent bill: \u20b9{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."'''

    target2 = '''    if any(k in text for k in ["quote", "pricing", "bill", "cost", "how much", "charges"]):
        if not any(item in text for item in ["cctv", "camera", "cameras", "ip", "static", "whatsapp", "sim", "backup", "pos", "router", "fiber", "speed"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
        return f"Here is your single transparent bill: \u20b9{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."'''

    replacement2 = '''    if (any(k in text for k in ["quote", "pricing", "cost", "how much", "charges", "monthly bill", "the bill"]) or any(w in text.split() for w in ["bill", "quote"])) and not any(w in text for w in ["billing", "billing software", "billing machine", "billing system"]):
        if not any(item in text for item in ["cctv", "camera", "cameras", "ip", "static", "whatsapp", "sim", "backup", "pos", "router", "fiber", "speed"]):
            transition_workflow(session_id, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
        return f"Here is your single transparent bill: \u20b9{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."'''

    assert target1 in content, "target1 not found"
    assert target2 in content, "target2 not found"

    content = content.replace(target1, replacement1, 1)
    content = content.replace(target2, replacement2, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated customer_workflow_engine.py")

if __name__ == "__main__":
    main()
