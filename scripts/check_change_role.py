with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function changeRole')
print(text[pos:pos+800])
