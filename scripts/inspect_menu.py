with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<ul class="sidebar-menu">')
end = text.find('</ul>', start)
print(text[start:end+5])
