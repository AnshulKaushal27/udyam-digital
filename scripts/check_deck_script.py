with open('E:/Airtel/scripts/generate_deck.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:60]):
    print(l, end='')
