with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'recommendation' in l or 'advisor/recommend' in l or 'evaluate' in l:
        print(f"{i+1}: {l.strip()}")
