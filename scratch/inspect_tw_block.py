with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos_tw = text.find('def transition_workflow')
pos_end_tw = text.find('return wf\n', pos_tw)
print("Length of transition_workflow:", pos_end_tw - pos_tw)
