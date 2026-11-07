with open('E:/Airtel/prototype/templates/control.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's count sections
sections = text.split('<section id="sec-quotes" style="display: none;">')
print(f"Found {len(sections)-1} occurrences of sec-quotes")

if len(sections) > 2:
    # Keep the first one and remove all subsequent duplicates
    first_part = sections[0] + '<section id="sec-quotes" style="display: none;">' + sections[1]
    
    # For remaining parts, strip out everything up to the next </section>
    cleaned_rest = []
    for s in sections[2:]:
        # find the end of this sec-quotes section
        end_idx = s.find('</section>')
        if end_idx != -1:
            cleaned_rest.append(s[end_idx + len('</section>'):])
        else:
            cleaned_rest.append(s)
            
    final_text = first_part + "".join(cleaned_rest)
    with open('E:/Airtel/prototype/templates/control.html', 'w', encoding='utf-8') as f:
        f.write(final_text)
    print("Successfully normalized to exactly 1 sec-quotes section!")
