with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def consumer_create_order' in l or 'consumer/order/create' in l:
        print(f"{i+1}: {l.strip()}")
