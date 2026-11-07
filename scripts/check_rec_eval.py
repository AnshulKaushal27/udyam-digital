with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('/api/recommendation/evaluate')
print(text[pos:pos+600])
