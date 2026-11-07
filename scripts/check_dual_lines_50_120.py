with open('E:/Airtel/scripts/test_dual_portals.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(50, min(120, len(lines))):
    print(lines[i], end='')
