import os
import re

profile_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\profile.html'

def update_profile_ui():
    with open(profile_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the User Card section
    # Search for the user card block and replace it with a more good/accurate standard edit UI
    
    label_start = '<label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Username</label>'
    
    # New UI block with Edit Icon and Alpine.js
    new_user_block = """                            <div>
                                <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Username</label>
                                <div class="flex items-center gap-3" x-data="{ editing: false, newUsername: '{{ user.username }}' }">
                                    <div x-show="!editing" class="flex-1 p-3 bg-gray-50 border-2 border-gray-100 rounded-xl font-medium text-gray-700 flex items-center justify-between group">
                                        <span x-text="newUsername"></span>
                                        <button @click="editing = true" class="p-1.5 hover:bg-red-50 text-gray-300 hover:text-red-700 rounded-lg transition-all">
                                            <i data-lucide="edit-3" class="w-4 h-4"></i>
                                        </button>
                                    </div>
                                    <form x-show="editing" method="post" class="flex-1 flex gap-2" @submit="editing = false">
                                        {% csrf_token %}
                                        <input type="text" name="username" x-model="newUsername" 
                                               class="p-3 bg-white border-2 border-red-200 rounded-xl font-medium text-gray-700 flex-1 focus:ring-2 focus:ring-red-100 focus:outline-none transition-all">
                                        <div class="flex gap-1">
                                            <button type="submit" class="p-3 bg-red-700 text-white rounded-xl shadow-md hover:bg-red-800 transition-all">
                                                <i data-lucide="check" class="w-4 h-4"></i>
                                            </button>
                                            <button type="button" @click="editing = false; newUsername = '{{ user.username }}'" class="p-3 bg-gray-100 text-gray-500 rounded-xl hover:bg-gray-200 transition-all">
                                                <i data-lucide="x" class="w-4 h-4"></i>
                                            </button>
                                        </div>
                                    </form>
                                </div>
                            </div>"""
    
    # Replace the existing username block (the one I added earlier)
    # The previous script replaced it with a form.
    content = re.sub(r'<div>\s*<label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Username</label>\s*<form.*?</form>\s*</div>', new_user_block, content, flags=re.DOTALL)

    # 2. Add Recent Summaries Section
    recent_summaries_block = """                <!-- Recent Summaries Section -->
                <div class="bg-white border-2 border-gray-100 shadow-xl rounded-2xl overflow-hidden mt-6">
                    <div class="bg-gradient-to-r from-red-50 to-orange-50 border-b-2 border-gray-100 p-6">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <i data-lucide="clock" class="w-5 h-5 text-red-700"></i>
                                <h2 class="text-lg font-bold">Recent Summaries</h2>
                                <span class="text-lg">📚</span>
                            </div>
                            <a href="/upload/" class="text-xs font-bold text-red-700 hover:underline">View All</a>
                        </div>
                    </div>
                    <div class="p-6">
                        {% if recent_summaries %}
                        <div class="space-y-4">
                            {% for summary in recent_summaries %}
                            <div class="flex items-center justify-between p-4 bg-gray-50 border-2 border-gray-100 rounded-2xl hover:border-red-100 transition-all group">
                                <div class="flex items-center gap-4">
                                    <div class="text-2xl">{{ summary.emoji }}</div>
                                    <div>
                                        <div class="font-bold text-sm text-gray-900 group-hover:text-red-700 transition-colors">{{ summary.file_name }}</div>
                                        <div class="text-[10px] text-gray-500 font-medium">{{ summary.created_at|date:"M d, Y" }}</div>
                                    </div>
                                </div>
                                <a href="/summarize/download/{{ summary.id }}/" class="p-2 bg-white rounded-xl shadow-sm text-gray-400 hover:text-red-700 hover:shadow-md transition-all">
                                    <i data-lucide="download" class="w-4 h-4"></i>
                                </a>
                            </div>
                            {% endfor %}
                        </div>
                        {% else %}
                        <div class="text-center py-8">
                            <div class="text-4xl mb-2 text-gray-200">📭</div>
                            <p class="text-sm text-gray-500">No summaries yet. <a href="/upload/" class="text-red-700 underline">Generate one now!</a></p>
                        </div>
                        {% endif %}
                    </div>
                </div>"""
                
    if 'Recent Summaries Section' not in content:
        content = content.replace('<!-- Account Achievements -->', recent_summaries_block + '\n\n                <!-- Account Achievements -->')
        # Also handle the variant if the comment is different
        if 'Recent Summaries Section' not in content:
             content = content.replace('<!-- Achievements -->', recent_summaries_block + '\n\n                <!-- Achievements -->')

    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated profile.html with new UI and Recent Summaries")

update_profile_ui()
