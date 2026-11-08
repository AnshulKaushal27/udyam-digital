with open(r"e:\Airtel\prototype\customer_workflow_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """    if stage == "KYC_VERIFICATION":
        if any(k in text for k in ["demo kyc", "test specimen", "specimen demo", "specimen verify", "07aaaaa"]):
            transition_workflow(session_id, "VERIFY_KYC_DEMO", {"gstin": "07AAAAA0000A1Z5"})
            return "Smart KYC Specimen Demo PASSED! Tested under simulated benchmark. Tracking is live on the left panel!"
        else:
            return "Please upload or capture your KYC document on the left panel, and confirm DPDP statutory consent. Our Smart KYC engine will verify it in real-time." """

# Let's search loosely for `if stage == "KYC_VERIFICATION":`
pos = text.find('if stage == "KYC_VERIFICATION":')
if pos != -1:
    end_pos = text.find('# ====================================================\n    # 8. INSTALLATION_TRACKING', pos)
    if end_pos == -1:
        end_pos = text.find('# 8. INSTALLATION_TRACKING', pos)
    
    new_block = """if stage == "KYC_VERIFICATION":
        if any(k in text for k in ["demo", "specimen", "07aaaaa"]):
            transition_workflow(session_id, "VERIFY_KYC_DEMO", {"gstin": "07AAAAA0000A1Z5"})
            return "Smart KYC Specimen Demo PASSED! Tested under simulated benchmark. Tracking is live on the left panel!"
        elif any(k in text for k in ["track", "status", "installation", "delivery", "order"]):
            if wf.get("kyc", {}).get("status") in ["APPROVED", "VERIFIED"]:
                transition_workflow(session_id, "GO_TO_STAGE", {"stage": "INSTALLATION_TRACKING"})
                return "Proceeding to installation tracking. Field engineer Rahul Sharma is on his way!"
            else:
                return "Cannot proceed to installation tracking yet. Please complete Smart KYC document verification first or test with specimen demo."
        else:
            return "Please upload or capture your KYC document on the left panel, and confirm DPDP statutory consent. Our Smart KYC engine will verify it in real-time."
    \n    """
    text = text[:pos] + new_block + text[end_pos:]
    with open(r"e:\Airtel\prototype\customer_workflow_engine.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully updated KYC chat block in customer_workflow_engine.py")
else:
    print("Could not find KYC stage block")
