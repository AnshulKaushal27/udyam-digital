import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = "    loadPartnerIntelligence();\n  </script>"

with open('E:/Airtel/scripts/patch_control_js.py', 'r', encoding='utf-8') as f:
    js_src = f.read()

# Extract new_js_code from patch_control_js.py
start = js_src.find('new_js_code = """') + len('new_js_code = """')
end = js_src.find('"""\n\nscript_end_marker')
new_js_code = js_src[start:end]

if target in html and 'function loadExecutiveOverview' not in html:
    html = html.replace(target, new_js_code + '\n    loadPartnerIntelligence();\n  </script>', 1)
    print("Inserted Phase 6 JavaScript functions successfully.")
else:
    print(f"Target found: {target in html}, Func present: {'function loadExecutiveOverview' in html}")

with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
    f.write(html)
