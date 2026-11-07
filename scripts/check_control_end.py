with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(len(lines)-60, len(lines)):
    line = lines[i].encode('ascii', 'replace').decode('ascii')
    print(f"{i+1}: {line}", end='')
