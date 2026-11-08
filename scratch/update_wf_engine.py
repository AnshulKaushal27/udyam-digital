with open(r'e:\Airtel\prototype\customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    if any(k in text for k in ["backup", "failover", "dual sim", "4g backup"]):
        action_name = "REMOVE_REQUIREMENT" if any(w in text for w in ["remove", "no backup", "don't need", "without"]) else "ADD_REQUIREMENT"
        transition_workflow(session_id, action_name, {"requirement": "upi_failover"})
        req_updated = True"""

replacement = """    if any(k in text for k in ["backup", "failover", "dual sim", "4g backup", "upi", "pos", "qr payments", "both upi & pos", "qr code", "card swipe"]):
        action_name = "REMOVE_REQUIREMENT" if any(w in text for w in ["remove", "no backup", "don't need", "without", "cash mainly", "no upi", "no pos"]) else "ADD_REQUIREMENT"
        transition_workflow(session_id, action_name, {"requirement": "upi_failover"})
        req_updated = True"""

assert target in text, 'Target not found'
text = text.replace(target, replacement, 1)

with open(r'e:\Airtel\prototype\customer_workflow_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated customer_workflow_engine.py successfully')
