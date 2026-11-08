with open("e:/Airtel/prototype/app.py", "r", encoding="utf-8") as f:
    text = f.read()

target = "    _recalculate_workflow_quote,\n    STAGES"
replacement = "    _recalculate_workflow_quote,\n    REQ_TO_PRODUCT_MAP,\n    STAGES"

text = text.replace(target, replacement, 1)

with open("e:/Airtel/prototype/app.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Added REQ_TO_PRODUCT_MAP import to app.py successfully!")
