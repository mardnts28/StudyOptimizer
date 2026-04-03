import os

views_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\views.py'

def fix_newlines():
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check what's actually there
    if ".replace('\\\\n', '<br/>')" in content:
        content = content.replace(".replace('\\\\n', '<br/>')", ".replace('\\n', '<br/>')")
    
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed newline replacement in PDF view")

fix_newlines()
