with open('E:/Airtel/submission/Solution_Architecture_and_Data_Flows.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if l.startswith('#'):
        print(f"{i+1}: {l.strip()}")
