"""Fix runaway LLM hallucination and repetition loop."""
with open(r'E:\Airtel\prototype\conversational_ai.py', 'r', encoding='utf-8') as f:
    c_ai = f.read()

# 1. Update build_proactive_sales_prompt in conversational_ai.py
old_indec = '''    # Indecision Instructions
    indecision_directive = (
        "CRITICAL INDECISION & DELEGATION POLICY:\\n"
        "1. If customer says 'Whatever is fine', 'You decide', 'I don't know', 'Jo marzi', 'Tusi hi dass do', or 'Kuch bhi chalega':\\n"
        "   - DO NOT ASK THE SAME PREFERENCE QUESTION AGAIN.\\n"
        "   - TAKE OWNERSHIP: Make a sensible, recommended business decision on their behalf (e.g. choose Cloud POS billing because it allows mobile/anywhere access).\\n"
        "   - Briefly state why, and move the conversation forward.\\n"
        "2. When customer needs digital billing/invoicing: Confirm manual vs software -> GST needs -> approximate monthly volume. "
        "   Once volume (~300-400 bills) is established, RECOMMEND Cloud-based billing immediately. DO NOT interrogate about cloud vs desktop.\\n"
        "3. NEVER ask the same question more than once if customer delegates or indicates indifference."
    )'''

new_indec = '''    # Strict Turn & Indecision Directives
    indecision_directive = (
        "CRITICAL CONVERSATIONAL RULES (ABSOLUTE NON-NEGOTIABLE):\\n"
        "1. You are speaking in REAL-TIME with an MSME customer. Output ONLY YOUR NEXT SINGLE MESSAGE (15 to 30 words maximum).\\n"
        "2. NEVER simulate the customer's responses. NEVER generate both sides of the conversation. Output ONLY what YOU say next!\\n"
        "3. ASK AT MOST ONE SINGLE QUESTION AT A TIME. Never ask multiple questions.\\n"
        "4. If customer mentions paper billing: acknowledge and ask ONLY whether they need GST-compliant invoices. Stop there!\\n"
        "5. If customer confirms GST invoices: ask ONLY approximately how many invoices they generate per month. Stop there!\\n"
        "6. If customer specifies volume (~300-400 bills): recommend Cloud POS & Billing (P19) at ₹599/month (setup ₹2,500) with AirFiber.\\n"
        "7. If customer expresses indecision ('Whatever is fine', 'You decide', 'Jo marzi', 'Tusi hi dass do'):\\n"
        "   - DO NOT ASK THE SAME PREFERENCE QUESTION AGAIN.\\n"
        "   - TAKE OWNERSHIP: Make a sensible recommendation on their behalf and advance.\\n"
        "8. NEVER ask the same question twice."
    )'''

assert old_indec in c_ai, "old_indec not found in conversational_ai.py"
c_ai = c_ai.replace(old_indec, new_indec, 1)

with open(r'E:\Airtel\prototype\conversational_ai.py', 'w', encoding='utf-8') as f:
    f.write(c_ai)

print("conversational_ai.py updated successfully!")
