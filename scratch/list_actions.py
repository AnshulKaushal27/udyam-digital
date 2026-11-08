import re

with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'action == "([A-Z_]+)"', text)
print(sorted(set(matches)))
