with open(r"e:\Airtel\prototype\app.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '"readability": vision_analysis.get("readability", "unprocessed"),'
replacement = '"readability": vision_analysis.get("readability", "unprocessed"),\n            "extracted_fields": vision_analysis.get("extracted_fields", {}),'

if target in text:
    text = text.replace(target, replacement, 1)
    with open(r"e:\Airtel\prototype\app.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully added extracted_fields to vision_analysis in app.py")
else:
    print("target not found")
