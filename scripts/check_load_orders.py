with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function loadLiveOrders')
print(text[pos:pos+1000])
