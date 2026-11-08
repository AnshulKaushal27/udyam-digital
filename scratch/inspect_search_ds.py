import os

for root, dirs, files in os.walk('e:/Airtel/prototype'):
    for f in files:
        if f.endswith('.py') or f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                c = fl.read()
                for line in c.splitlines():
                    if 'Digital Starter' in line or ('Selected' in line and 'Kirana' in line):
                        print(f"{p}: {line[:100].encode('ascii', 'replace').decode('ascii')}")
