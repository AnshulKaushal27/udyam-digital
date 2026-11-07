with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

def show_section(sec_id):
    start = text.find(f'id="{sec_id}"')
    if start != -1:
        print(f"=== {sec_id} (first 800 chars) ===")
        print(text[start:start+800])
        print("\n")

show_section('sec-overview')
show_section('sec-insights')
