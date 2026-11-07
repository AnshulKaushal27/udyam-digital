with open('E:/Airtel/scripts/generate_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('SLIDE 7:')
print(text[pos+2500:pos+3800])
