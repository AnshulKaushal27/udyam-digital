with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('<!-- Right: Live Itemized Quote Bill -->')
if pos == -1:
    pos = text.find('rec.monthly_subtotal')
print(text[pos-100:pos+2500].encode('ascii', 'replace').decode('ascii'))
