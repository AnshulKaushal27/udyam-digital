with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sections = re.findall(r'<section[^>]+id=[\'"]([^\'"]+)[\'"][^>]*>', text)
print("Sections found:", sections)
