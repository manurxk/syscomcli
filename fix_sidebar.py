import re

with open('app/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace {{ "{{ with {{
# Replace }}" }} with }}
fixed_content = content.replace('{{ "{{', '{{').replace('}}" }}', '}}')

with open('app/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)
print("FIXED")
