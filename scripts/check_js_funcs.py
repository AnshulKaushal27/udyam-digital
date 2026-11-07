with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
print("JavaScript functions in control.html:", funcs)
