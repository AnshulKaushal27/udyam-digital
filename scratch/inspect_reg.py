with open('e:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('/api/auth/register')
print(text[pos:pos+1500])
