with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(183, 260):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
