import re

with open('E:/Airtel/scripts/test_operations_intelligence.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('assert r_empty.json()["status"] == "empty"', 'assert r_empty.json()["detailed_funnel"]["status"] == "empty"')

with open('E:/Airtel/scripts/test_operations_intelligence.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Test 15 assertion.")
