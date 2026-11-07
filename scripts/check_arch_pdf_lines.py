with open('E:/Airtel/scripts/generate_architecture_pdf.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(40, 110):
    print(lines[i], end='')
