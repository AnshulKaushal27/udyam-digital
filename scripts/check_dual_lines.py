with open('E:/Airtel/scripts/test_dual_portals.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(min(50, len(lines))):
    print(lines[i], end='')
