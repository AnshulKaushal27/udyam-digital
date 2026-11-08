with open(r"E:\Airtel\prototype\app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update SHARED_ORDERS ORD-2026-9812 source & flags
old_source = '"source": "Consumer Portal (Self-Serve)"'
new_source = '"source": "Seeded Demo Record (Harmony Dental Care)",\n        "is_seeded": True,\n        "is_demo": True,\n        "is_seeded_demo": True'
assert old_source in content, "old_source not found"
content = content.replace(old_source, new_source, 1)

# 2. Update executive overview call to pass WORKFLOW_SESSIONS
old_exec_call = "overview = get_executive_overview(SHARED_ORDERS, SHARED_QUOTES, RECOVERY_RECORDS, KYC_AUDIT_TRAIL)"
new_exec_call = "overview = get_executive_overview(SHARED_ORDERS, SHARED_QUOTES, RECOVERY_RECORDS, KYC_AUDIT_TRAIL, WORKFLOW_SESSIONS)"
assert old_exec_call in content, "old_exec_call not found"
content = content.replace(old_exec_call, new_exec_call, 1)

# 3. Remove avg_simulated_tat_days: 2.8
old_tat_stat = '"avg_simulated_tat_days": 2.8'
new_tat_stat = '"avg_simulated_tat_days": None,\n            "tat_status": "Unavailable (Requires completed activations with timestamps)"'
assert old_tat_stat in content, "old_tat_stat not found"
content = content.replace(old_tat_stat, new_tat_stat, 1)

# 4. Set activated_at when milestone 5 is reached
old_step5 = 'if target_step == 5:'
new_step5 = 'if target_step == 5:\n        order["activated_at"] = datetime.now().strftime("%d-%b-%Y %H:%M IST")'
assert old_step5 in content, "old_step5 not found"
content = content.replace(old_step5, new_step5, 1)

# 5. Add is_hypothesis to compat_insights
old_compat = '"business_implication": item["business_implication"]'
new_compat = '"business_implication": item["business_implication"],\n            "is_hypothesis": item.get("is_hypothesis", False),\n            "traceable_source": item.get("traceable_source", "")'
assert old_compat in content, "old_compat not found"
content = content.replace(old_compat, new_compat, 1)

# 6. Mark seeded quotes
content = content.replace('"quote_id": "QTE-2026-9812",', '"quote_id": "QTE-2026-9812",\n        "is_seeded": True,\n        "is_seeded_demo": True,', 1)
content = content.replace('"quote_id": "QTE-2026-4410",', '"quote_id": "QTE-2026-4410",\n        "is_seeded": True,\n        "is_seeded_demo": True,', 1)
content = content.replace('"quote_id": "QTE-2026-1189",', '"quote_id": "QTE-2026-1189",\n        "is_seeded": True,\n        "is_seeded_demo": True,', 1)

with open(r"E:\Airtel\prototype\app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("app.py successfully patched.")
