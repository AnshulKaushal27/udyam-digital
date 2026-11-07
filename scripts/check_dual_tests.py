with open('E:/Airtel/scripts/test_dual_portals.py', 'r', encoding='utf-8') as f:
    text = f.read()

for line in text.split('\n'):
    if 'analytics' in line or 'funnel' in line or 'insights' in line:
        print(line)
