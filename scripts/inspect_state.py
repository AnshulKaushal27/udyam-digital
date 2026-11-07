import os
import re

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'id=[\'"](sec-[^\'"]+)[\'"]', text)
print("Sections in control.html:", sections)

# Also check navigation items
nav_items = re.findall(r'nav-link[^>]*data-target=[\'"]([^\'"]+)[\'"]', text)
print("Nav links in control.html:", nav_items)
