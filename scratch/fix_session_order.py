with open(r'prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    if message:
        detected_lang = detect_natural_language_switch(message)
        if detected_lang:
            lang = detected_lang
            session["profile"]["preferred_language"] = lang
            wf["language"] = lang

    # 1. Fetch & sync authoritative state
    wf = get_or_create_workflow(sid, language=lang)
    session = get_or_create_session(sid, raw_cat or wf.get("discovery", {}).get("business_type", "kirana"), lang)
    sync_workflow_to_session(sid)
    stage = wf.get("stage", "REQUIREMENTS_COLLECTION")'''

replacement = '''    # 1. Fetch authoritative state
    wf = get_or_create_workflow(sid, language=lang)
    session = get_or_create_session(sid, raw_cat or wf.get("discovery", {}).get("business_type", "kirana"), lang)

    # 2. Natural language switch detection
    if message:
        detected_lang = detect_natural_language_switch(message)
        if detected_lang:
            lang = detected_lang
            session["profile"]["preferred_language"] = lang
            wf["language"] = lang

    sync_workflow_to_session(sid)
    stage = wf.get("stage", "REQUIREMENTS_COLLECTION")'''

assert target in text, "Target not found"
text = text.replace(target, replacement, 1)

with open(r'prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed session initialization order in app.py successfully")
