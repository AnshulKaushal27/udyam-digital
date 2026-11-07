with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:300]):
    if 'SHARED_ORDERS' in l or 'ORD-2026' in l:
        print(f"{i+1}: {l.strip()}")
