import os

for root, dirs, files in os.walk('e:/Airtel/prototype'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                if 'extract_and_update_profile' in fl.read():
                    print('Found in:', p)
