with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function initWorkflow')
print(text[pos:pos+1500].encode('ascii', 'replace').decode('ascii'))
