with open(r'e:\Airtel\prototype\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'app.config["TEMPLATES_AUTO_RELOAD"] = True'
replacement = '''app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response'''

assert target in text, 'Target not found'
text = text.replace(target, replacement, 1)

with open(r'e:\Airtel\prototype\app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added no-cache headers to app.py successfully')
