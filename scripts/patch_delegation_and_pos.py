def main():
    path = "prototype/customer_workflow_engine.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add delegation check in USER_TYPE_SELECTION
    target1 = '''    if stage == "USER_TYPE_SELECTION":
        if any(k in text for k in ["business", "business owner", "customer", "merchant", "dukaan", "shop", "store", "grocery", "run a", "own a business", "store owner", "businessman", "entrepreneur", "retailer", "client", "msme", "smb", "1", "option 1"]) and not any(w in text for w in ["airtel employee", "internal staff", "airtel team"]):
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "customer"})
            return "Noted! Welcome, business owner. Are you already an Airtel Business customer?"'''

    replacement1 = '''    if stage == "USER_TYPE_SELECTION":
        if any(k in text for k in ["you decide", "what is best", "best for my", "recommend", "aap batao", "tum batao", "suggest", "which plan", "confused", "dont know", "don't know", "what should i choose"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
            return "I recommend our Kirana Digital Starter with plug-and-play AirFiber and automatic 4G backup SIM. It is our most popular option engineered to ensure zero payment dropouts."

        if any(k in text for k in ["business", "business owner", "customer", "merchant", "dukaan", "shop", "store", "grocery", "run a", "own a business", "store owner", "businessman", "entrepreneur", "retailer", "client", "msme", "smb", "1", "option 1"]) and not any(w in text for w in ["airtel employee", "internal staff", "airtel team"]):
            transition_workflow(session_id, "SELECT_USER_TYPE", {"user_type": "customer"})
            return "Noted! Welcome, business owner. Are you already an Airtel Business customer?"'''

    # 2. Refine kirana category keywords (remove standalone 'pos')
    target2 = '''        if any(k in text for k in ["kirana", "grocery", "retail", "general store", "provision", "dukaan", "supermarket", "pos", "counter"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
            return "Selected Kirana & Retail. How many staff or devices do you have, and what challenges do you face with Wi-Fi, payments, or security?"'''

    replacement2 = '''        if any(k in text for k in ["kirana", "grocery", "general store", "provision", "dukaan", "supermarket", "retail store", "retail shop", "retail business"]) or text in ["retail", "kirana", "1", "option 1"]:
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
            return "Selected Kirana & Retail. How many staff or devices do you have, and what challenges do you face with Wi-Fi, payments, or security?"'''

    assert target1 in content, "target1 not found"
    assert target2 in content, "target2 not found"

    content = content.replace(target1, replacement1, 1)
    content = content.replace(target2, replacement2, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated customer_workflow_engine.py with delegation and refined category matching")

if __name__ == "__main__":
    main()
