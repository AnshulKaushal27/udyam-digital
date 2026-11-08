with open(r'prototype/conversational_ai.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update is_speed_need in interpret_user_intent_fallback
target1 = '''    is_speed_need = any(k in text_low for k in [
        "tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi",
        "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber",
        "fibre", "symmetrical", "buffering", "speed chahiye"
    ])'''

replacement1 = '''    is_speed_need = any(k in text_low for k in [
        "tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi",
        "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber",
        "fibre", "symmetrical", "buffering", "speed chahiye",
        "तेज इंटरनेट", "इंटरनेट", "हाई स्पीड", "स्पीड", "वाईफाई", "फास्ट इंटरनेट",
        "ਤੇਜ਼ ਇੰਟਰਨੈੱਟ", "ਇੰਟਰਨੈੱਟ", "ਹਾਈ ਸਪੀਡ", "ਸਪੀਡ", "ਵਾਈ-ਫਾਈ"
    ])'''

assert target1 in text, "target1 not found"
text = text.replace(target1, replacement1, 1)

# 2. Update is_speed_need in generate_deterministic_consultant_reply if present
target2 = 'is_speed_need = any(k in text_low for k in ["tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi", "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber", "fibre", "symmetrical", "buffering", "speed chahiye"])'
replacement2 = 'is_speed_need = any(k in text_low for k in ["tez internet", "fast internet", "faster internet", "faster wifi", "faster wi-fi", "internet slow", "slow internet", "high speed", "speed", "bandwidth", "fiber", "fibre", "symmetrical", "buffering", "speed chahiye", "तेज इंटरनेट", "इंटरनेट", "हाई स्पीड", "स्पीड", "वाईफाई", "फास्ट इंटरनेट", "ਤੇਜ਼ ਇੰਟਰਨੈੱਟ", "ਇੰਟਰਨੈੱਟ", "ਹਾਈ ਸਪੀਡ", "ਸਪੀਡ", "ਵਾਈ-ਫਾਈ"])'

if target2 in text:
    text = text.replace(target2, replacement2, 1)

with open(r'prototype/conversational_ai.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Hindi/Punjabi keywords in conversational_ai.py successfully")
