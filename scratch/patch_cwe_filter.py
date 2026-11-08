with open("e:/Airtel/prototype/customer_workflow_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '''    active_addons = [
        aid for aid in active_addons
        if (aid not in all_mapped_pids or aid in pids_from_reqs) and aid not in bundle_included_pids
    ]'''

replacement = '''    active_addons = [
        aid for aid in active_addons
        if (aid not in all_mapped_pids or aid in pids_from_reqs)
    ]'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open("e:/Airtel/prototype/customer_workflow_engine.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated customer_workflow_engine.py active_addons filter successfully!")
else:
    print("Target not found in customer_workflow_engine.py!")
