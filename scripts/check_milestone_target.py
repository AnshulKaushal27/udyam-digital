with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'target_step == 5' in l:
        print(f"{i+1}: {l.strip()}")
        for j in range(max(0, i-5), min(len(lines), i+6)):
            print(f"  {j+1}: {lines[j]}", end='')
