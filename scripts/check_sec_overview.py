with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="sec-overview"')
end = text.find('</section>', start)
print(text[start:start+1500])
