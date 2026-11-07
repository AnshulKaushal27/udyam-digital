with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="sec-kyc"')
print(text[pos:pos+1200])
