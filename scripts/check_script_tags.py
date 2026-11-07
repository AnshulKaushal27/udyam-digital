with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<script', text)]
print("Script tag positions:", matches)
for pos in matches:
    print(text[pos:pos+150])
    print("-" * 40)
