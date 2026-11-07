with open('E:/Airtel/scripts/generate_deck.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)-35, len(lines)):
    print(lines[i], end='')
