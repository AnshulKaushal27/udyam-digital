"""Fix user_part unbound error and ensure meta is always emitted."""
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

target = '''        else:
            parsed_meta = {}
            if meta_buffer:
                try:
                    clean_meta = meta_buffer.strip().replace("```json", "").replace("```", "")
                    parsed_meta = json.loads(clean_meta)
                except Exception:
                    pass

            if not parsed_meta.get("quick_replies"):
                parsed_meta["quick_replies"] = get_contextual_quick_replies(session, last_user_text, parsed_meta.get("discovery_complete", False), user_part)'''

replacement = '''        else:
            # Emit any remaining unemitted conversational text if delimiter was not present
            if not meta_started:
                user_part = accumulated.strip()
                unemitted = accumulated[emitted_len:]
                if unemitted:
                    yield f"data: {json.dumps({'type': 'chunk', 'text': unemitted})}\\n\\n"
                    emitted_len += len(unemitted)
            else:
                user_part = user_part if 'user_part' in locals() else accumulated.split(delimiter)[0].strip()

            parsed_meta = {}
            if meta_buffer:
                try:
                    clean_meta = meta_buffer.strip().replace("```json", "").replace("```", "")
                    parsed_meta = json.loads(clean_meta)
                except Exception:
                    pass

            if not parsed_meta.get("quick_replies"):
                parsed_meta["quick_replies"] = get_contextual_quick_replies(session, last_user_text, parsed_meta.get("discovery_complete", False), user_part)'''

assert target in app_code, "target not found in app.py"
app_code = app_code.replace(target, replacement, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Fixed user_part and meta emission in app.py successfully!")
