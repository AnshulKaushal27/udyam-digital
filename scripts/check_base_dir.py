with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(65, 82):
    print(f"{i+1}: {lines[i]}", end='')
