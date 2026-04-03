import os

profile_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\profile.html'
collaborate_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\collaborate.html'
upload_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\upload.html'

def add_messages(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '{% if messages %}' in content:
        return
    
    messages_block = """    {% if messages %}
    <div class="max-w-5xl mx-auto px-6 mt-4 space-y-2">
        {% for message in messages %}
        <div class="p-4 rounded-xl font-bold text-sm {% if message.tags == 'error' %}bg-red-50 text-red-700 border-2 border-red-100{% elif message.tags == 'success' %}bg-green-50 text-green-700 border-2 border-green-100{% else %}bg-blue-50 text-blue-700 border-2 border-blue-100{% endif %}">
            {{ message }}
        </div>
        {% endfor %}
    </div>
    {% endif %}"""
    
    # Insert after nav
    nav_end = '</nav>'
    if nav_end in content:
        index = content.find(nav_end) + len(nav_end)
        new_content = content[:index] + "\n" + messages_block + content[index:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added messages to {os.path.basename(path)}")

add_messages(profile_path)
add_messages(collaborate_path)
add_messages(upload_path)
