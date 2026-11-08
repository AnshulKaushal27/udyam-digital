with open('e:/Airtel/prototype/templates/consumer.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function dispatchWorkflowTransition')
if pos == -1:
    pos = text.find('dispatchWorkflowTransition')
print(text[pos:pos+2500].encode('ascii', 'replace').decode('ascii'))
