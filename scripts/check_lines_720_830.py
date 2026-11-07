with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(720, 830):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
