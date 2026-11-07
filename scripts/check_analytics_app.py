with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# find where /api/control/analytics/funnel is defined
pos = text.find('/api/control/analytics/funnel')
print(text[pos-100:pos+800])
