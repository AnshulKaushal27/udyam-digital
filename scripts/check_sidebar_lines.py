with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(180, 260):
    line = lines[i].encode('ascii', 'replace').decode('ascii')
    print(f"{i+1}: {line}", end='')
