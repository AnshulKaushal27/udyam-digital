with open('e:/Airtel/prototype/customer_workflow_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos_recalc = text.find('def _recalculate_workflow_quote')
pos_recalc_end = text.find('def get_visible_gui_options', pos_recalc)
print("=== RECALC BLOCK ===")
print(text[pos_recalc:pos_recalc_end].encode('ascii', 'replace').decode('ascii'))
