with open(r'e:\Airtel\prototype\conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    else: # Kirana / Micro
        if msg_count <= 2:"""

replacement = """    else: # Kirana / Micro
        has_payment_mentioned = any(k in text_low for k in ["upi", "pos", "qr", "cash", "payment", "card", "swipe", "scanner", "gpay", "phonepe", "paytm"])
        if has_payment_mentioned or msg_count > 2:
            target_bundle = "prod_p19_pos"
            if "cash" in text_low and not any(k in text_low for k in ["upi", "pos", "qr"]):
                reply = "Understood! For cash-centric retail, our high-speed Fiber ensures your store accounting and billing stay uninterrupted."
            else:
                reply = "Understood! AirFiber with automatic 4G failover ensures your shop's UPI QR and card machines never drop during evening rush."
            quick = ["View Package Details", "Check Installation SLA", "Request Callback"]
            return reply, quick, target_bundle, True, "Plug-and-play wireless AirFiber with auto 4G failover guarantees zero UPI/POS transaction drops."
        if msg_count <= 2:"""

assert target in text, 'Target not found'
text = text.replace(target, replacement, 1)

with open(r'e:\Airtel\prototype\conversational_ai.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated conversational_ai.py successfully')
