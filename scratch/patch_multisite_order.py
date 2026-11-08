def main():
    path = "prototype/customer_workflow_engine.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    target = '''    if stage in ["BUSINESS_IDENTIFICATION", "USER_TYPE_SELECTION", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_SIGNUP", "CUSTOMER_LOGIN"]:
        if any(k in text for k in ["kirana", "grocery", "retail", "general store", "provision", "dukaan", "supermarket", "pos", "counter"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
            return "Selected Kirana & Retail. How many staff or devices do you have, and what challenges do you face with Wi-Fi, payments, or security?"

        if any(k in text for k in ["clinic", "doctor", "dental", "dentist", "hospital", "pathology", "lab", "ca office", "consultant", "lawyer", "office", "swasthya"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "clinic"})
            return "Selected Clinic & Professional Office Suite. Do you require cloud records backup and high uptime Wi-Fi?"

        if any(k in text for k in ["multisite", "multi site", "multi-store", "chain", "branches", "multiple outlets", "multiple stores"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "multisite"})
            return "Selected Multi-Site Retail Pro. SD-WAN failover and central CCTV are included."'''

    replacement = '''    if stage in ["BUSINESS_IDENTIFICATION", "USER_TYPE_SELECTION", "CUSTOMER_ACCOUNT_CHECK", "CUSTOMER_SIGNUP", "CUSTOMER_LOGIN"]:
        if any(k in text for k in ["multisite", "multi site", "multi-store", "chain", "branches", "multiple outlets", "multiple stores", "expanded to"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "multisite"})
            return "Selected Multi-Site Retail Pro. SD-WAN failover and central CCTV are included."

        if any(k in text for k in ["clinic", "doctor", "dental", "dentist", "hospital", "pathology", "lab", "ca office", "consultant", "lawyer", "office", "swasthya"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "clinic"})
            return "Selected Clinic & Professional Office Suite. Do you require cloud records backup and high uptime Wi-Fi?"

        if any(k in text for k in ["kirana", "grocery", "retail", "general store", "provision", "dukaan", "supermarket", "pos", "counter"]):
            transition_workflow(session_id, "SELECT_CATEGORY", {"category": "kirana"})
            return "Selected Kirana & Retail. How many staff or devices do you have, and what challenges do you face with Wi-Fi, payments, or security?"'''

    assert target in content, "Target block not found"
    new_content = content.replace(target, replacement, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated customer_workflow_engine.py with multisite priority")

if __name__ == "__main__":
    main()
