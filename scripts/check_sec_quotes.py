with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="sec-quotes"')
print(text[pos:pos+1200])
