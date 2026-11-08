with open(r'prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = 'is_add = any(k in text_low for k in ["add ", "include ", "chahiye", "add kar", "daal do", "yes, add", "yes add", "please add"])'
replacement1 = 'is_add = any(k in text_low for k in ["add ", "include ", "add kar", "daal do", "yes, add", "yes add", "please add"]) or any(k in text_low for k in ["cctv chahiye", "static ip chahiye", "sim chahiye"])'

assert target1 in text, "target1 not found"
text = text.replace(target1, replacement1, 1)

target2 = 'if any(k in text_low for k in ["airfiber", "broadband", "internet", "wifi"]):'
replacement2 = 'if any(k in text_low for k in ["airfiber", "air fiber", "add airfiber", "include airfiber"]):'

assert target2 in text, "target2 not found"
text = text.replace(target2, replacement2, 1)

with open(r'prototype/conversational_ai.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated parse_quote_action_intent in conversational_ai.py")
