with open(r'e:\Airtel\prototype\recovery_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''        # Ownership & Lifecycle
        "recovery_status": "draft_ready", # draft_ready, contacted, recovered, closed_lost, opted_out'''

replacement1 = '''        # Provenance & Data Origin
        "is_seeded": bool(profile.get("is_seeded", False) or "seed" in str(session_id).lower()),
        "record_origin": "Seeded Benchmark Example" if (profile.get("is_seeded", False) or "seed" in str(session_id).lower()) else "Live Customer Abandonment",

        # Ownership & Lifecycle
        "recovery_status": "draft_ready", # draft_ready, contacted, recovered, closed_lost, opted_out'''

assert target1 in text, "target1 not found in recovery_engine.py"
text = text.replace(target1, replacement1, 1)

with open(r'e:\Airtel\prototype\recovery_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated recovery_engine.py with record provenance and seeded labeling successfully")
