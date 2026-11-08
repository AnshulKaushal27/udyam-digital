with open("e:/Airtel/prototype/conversational_ai.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '''        active_addons_in_quote = [a.get("addon_key") or a.get("id") for a in current_quote.get("addons", [])] if current_quote else []'''

replacement = '''        active_addons_in_quote = []
        if current_quote:
            for a in current_quote.get("addons", []):
                if isinstance(a, dict):
                    active_addons_in_quote.append(a.get("addon_key") or a.get("id"))
                elif isinstance(a, str):
                    active_addons_in_quote.append(a)
            for sa in current_quote.get("selected_addons", []):
                if isinstance(sa, dict):
                    active_addons_in_quote.append(sa.get("addon_key") or sa.get("id"))
                elif isinstance(sa, str):
                    active_addons_in_quote.append(sa)'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open("e:/Airtel/prototype/conversational_ai.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated conversational_ai.py active_addons_in_quote successfully!")
else:
    print("Target not found in conversational_ai.py!")
