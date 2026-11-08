with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    if message:
        detected_lang = detect_natural_language_switch(message)
        if detected_lang:
            lang = detected_lang'''

replacement = '''    if message:
        detected_lang = detect_natural_language_switch(message)
        if detected_lang:
            lang = detected_lang
            session["profile"]["preferred_language"] = lang
            wf["language"] = lang'''

assert target in text, "Target not found"
text = text.replace(target, replacement, 1)

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated natural language switch profile update in app.py")
