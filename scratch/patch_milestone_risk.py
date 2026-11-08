with open('E:/Airtel/prototype/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = "    # Phase 4: Order Activation Commission Trigger\n    if target_step == 5:"
target_crlf = "    # Phase 4: Order Activation Commission Trigger\r\n    if target_step == 5:"

replacement = "    # Phase 6: Proactive Installation Risk Engine recalculation on milestone change\r\n    order[\"installation\"][\"risk_assessment\"] = evaluate_order_risk(order)\r\n\r\n    # Phase 4: Order Activation Commission Trigger\r\n    if target_step == 5:"

if target_crlf in text:
    text = text.replace(target_crlf, replacement, 1)
    print("Replaced CRLF target successfully.")
elif target in text:
    text = text.replace(target, replacement, 1)
    print("Replaced LF target successfully.")
else:
    print("Neither target found.")

with open('E:/Airtel/prototype/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
