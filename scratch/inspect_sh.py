with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 0
while True:
    pos = text.find('stage_history', pos)
    if pos == -1: break
    print(text[max(0, pos-40):pos+60])
    pos += 1
