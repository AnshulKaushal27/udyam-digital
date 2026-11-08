"""Fix quick_replies resolution order in advisor_chat_stream."""
with open(r'E:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

target = '''            if not parsed_meta.get("quick_replies"):
                parsed_meta["quick_replies"] = get_contextual_quick_replies(session, last_user_text, parsed_meta.get("discovery_complete", False), user_part)

            # Merge LLM metadata updates into profile
            extract_and_update_profile(session, last_user_text, parsed_meta)

            # Re-evaluate discovery completion deterministically
            is_complete = check_discovery_completion(profile, session["identified_needs"], user_count, last_user_text, session)
            if parsed_meta.get("discovery_complete") or is_complete:
                parsed_meta["discovery_complete"] = True
                parsed_meta["recommend_bundle"] = target_bundle_id'''

replacement = '''            # Merge LLM metadata updates into profile
            extract_and_update_profile(session, last_user_text, parsed_meta)

            # Re-evaluate discovery completion deterministically
            is_complete = check_discovery_completion(profile, session["identified_needs"], user_count, last_user_text, session)
            if parsed_meta.get("discovery_complete") or is_complete:
                parsed_meta["discovery_complete"] = True
                parsed_meta["recommend_bundle"] = target_bundle_id

            if not parsed_meta.get("quick_replies"):
                parsed_meta["quick_replies"] = get_contextual_quick_replies(session, last_user_text, parsed_meta.get("discovery_complete", False), user_part)'''

assert target in app_code, "target not found in app.py"
app_code = app_code.replace(target, replacement, 1)

with open(r'E:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Order fixed in app.py!")
