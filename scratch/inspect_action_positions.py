with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('elif action == "ADD_REQUIREMENT":')
pos2 = text.find('elif action == "SELECT_PLAN":')
pos3 = text.find('elif action == "TOGGLE_ADDON":')
pos4 = text.find('elif action == "GO_TO_STAGE":')
pos5 = text.find('elif action in ["PREVIOUS_STAGE", "GO_BACK"]:')
pos6 = text.find('elif action == "SET_LANGUAGE":')

print("pos1 (ADD_REQ):", pos1)
print("pos2 (SELECT_PLAN):", pos2)
print("pos3 (TOGGLE_ADDON):", pos3)
print("pos4 (GO_TO_STAGE):", pos4)
print("pos5 (PREV_STAGE):", pos5)
print("pos6 (SET_LANG):", pos6)
