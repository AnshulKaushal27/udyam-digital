with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:120]):
    if 'smb_leads' in l or 'csv' in l or 'LEADS' in l:
        print(f"{i+1}: {l.strip()}")
