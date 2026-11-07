with open('E:/Airtel/submission/Solution_Architecture_and_Data_Flows.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(175, len(lines)):
    print(lines[i], end='')
