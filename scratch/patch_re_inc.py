# Remove the `if addon_meta["id"] in bundle_product_ids: continue` check from calculate_quote_pricing
with open("e:/Airtel/prototype/recommendation_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '''        if addon_meta:
            # If product is already included in base bundle, do not double-charge!
            if addon_meta["id"] in bundle_product_ids:
                continue

            # Enforce dependency'''

replacement = '''        if addon_meta:
            # Enforce dependency'''

if target in text:
    text = text.replace(target, replacement, 1)

# In the included products loop in calculate_quote_pricing:
# If a product is in addon_items, don't also list it as included $0
target_inc = '''    for p in bundle.get("products", []):
        if p["id"] != base_prod_id:
            line_items.append({'''

replacement_inc = '''    addon_pids_set = {item["id"] for item in addon_items}
    for p in bundle.get("products", []):
        if p["id"] != base_prod_id and p["id"] not in addon_pids_set:
            line_items.append({'''

if target_inc in text:
    text = text.replace(target_inc, replacement_inc, 1)

with open("e:/Airtel/prototype/recommendation_engine.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated recommendation_engine.py successfully!")
