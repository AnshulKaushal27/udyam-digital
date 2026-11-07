import re

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find sidebar elements
sidebar = text[text.find('sidebar'):text.find('sidebar')+2000]
print(sidebar)
