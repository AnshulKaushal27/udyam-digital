with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="roleSelector"')
print(text[pos-100:pos+500].encode('ascii', 'replace').decode('ascii'))
