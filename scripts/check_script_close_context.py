with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 150353
print(repr(text[pos-100:pos+20]))
