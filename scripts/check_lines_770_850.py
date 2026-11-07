with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(770, 850):
    if i < len(lines):
        line = lines[i].encode('ascii', 'replace').decode('ascii')
        print(f"{i+1}: {line}", end='')
