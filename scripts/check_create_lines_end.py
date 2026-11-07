with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(540, 590):
    line = lines[i].encode('ascii', 'replace').decode('ascii')
    print(f"{i+1}: {line}", end='')
