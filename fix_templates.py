import os
import re

collaborate_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\collaborate.html'
profile_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\profile.html'

def fix_collaborate():
    with open(collaborate_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Top Contributors block
    # Search for the Top Contributors header and the following div
    # This might be tricky with regex if it's nested
    
    # We want to replace from lines 178 to 207 approximately
    # Let's find: <div class="p-4 space-y-4">
    # And replace everything until its closing div
    
    start_tag = '<div class="p-4 space-y-4">'
    # This is not enough because there are other such divs. 
    # Let's find "Top Contributors" first.
    
    if 'Top Contributors' in content:
        # Find the div that starts after Top Contributors
        header_index = content.find('Top Contributors')
        div_start = content.find(start_tag, header_index)
        if div_start != -1:
            # Now find the corresponding end div. This is hard without a parser.
            # But the hardcoded part had 4 contributors. 
            # We can just match the hardcoded block.
            
            hardcoded_block = content[div_start:content.find('<!-- Hot Topics -->', div_start)]
            # Trim the last </div>
            hardcoded_block = hardcoded_block[:hardcoded_block.rfind('</div>')]
            
            replacement = """                    <div class="p-4 space-y-4">
                        {% if top_contributors %}
                            {% for contributor in top_contributors %}
                                <div class="flex items-center gap-3">
                                    <span class="text-xl">
                                        {% if forloop.counter == 1 %}🥇
                                        {% elif forloop.counter == 2 %}🥈
                                        {% elif forloop.counter == 3 %}🥉
                                        {% else %}{{ forloop.counter }}️⃣{% endif %}
                                    </span>
                                    <div class="flex-1">
                                        <div class="font-semibold text-sm text-gray-900">{{ contributor.username }}</div>
                                        <div class="text-[10px] text-gray-500 font-bold uppercase tracking-tighter">{{ contributor.points }} Points • {{ contributor.materials }} Shares</div>
                                    </div>
                                </div>
                            {% endfor %}
                        {% else %}
                            <p class="text-xs text-gray-500 italic text-center py-4">No contributors yet. Be the first! 🌟</p>
                        {% endif %}
                    </div>"""
            
            new_content = content.replace(hardcoded_block, replacement)
            with open(collaborate_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Fixed collaborate.html")

def fix_profile():
    with open(profile_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_block = """                                <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Username</label>
                                <div class="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl font-medium text-gray-700">{{ user.username }}</div>"""
    
    new_block = """                                <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Username</label>
                                <form method="post" class="flex gap-2">
                                    {% csrf_token %}
                                    <input type="text" name="username" value="{{ user.username }}" 
                                           class="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl font-medium text-gray-700 flex-1 focus:border-red-400 focus:outline-none transition-all">
                                    <button type="submit" class="px-4 py-2 bg-gradient-to-r from-red-700 to-red-500 text-white rounded-xl font-bold text-xs shadow-md hover:shadow-lg transition-all">
                                        Update
                                    </button>
                                </form>"""
    
    if old_block in content:
        new_content = content.replace(old_block, new_block)
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed profile.html")
    else:
        # Try a more partial match if exact didn't work
        print("Could not find exact block in profile.html, trying regex...")
        new_content = re.sub(r'<label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Username</label>\s*<div class="p-3 bg-gray-50 border-2 border-gray-100 rounded-xl font-medium text-gray-700">\{\{ user\.username \}\}</div>', new_block, content)
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Regex replaced in profile.html")

fix_collaborate()
fix_profile()
