with open('E:/Airtel/scripts/test_discovery_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(125, 150):
    print(f"{i+1}: {lines[i]}", end='')
