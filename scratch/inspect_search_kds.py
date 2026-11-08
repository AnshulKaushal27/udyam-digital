import os

for root, dirs, files in os.walk('e:/Airtel/prototype'):
    for f in files:
        if f.endswith('.py') or f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                if 'Selected Kirana Digital Starter' in c:
                    print('Found in:', p)
