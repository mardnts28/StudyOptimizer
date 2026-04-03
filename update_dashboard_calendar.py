import os
import re

dashboard_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\dashboard.html'

def update_dashboard():
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the state in dashboardApp
    # newSchedule: { day: '', time: '', activity: '', color: 'blue' }
    content = content.replace("newSchedule: { day: '', time: '', activity: '', color: 'blue' },", 
                              "newSchedule: { day: '', date: '', time: '', activity: '', color: 'blue' },")

    # 2. Update the modal form to include a date picker
    # Replacing the select [Day] with [Day] and [Date]
    form_old = """                            <select x-model="newSchedule.day" class="w-full text-xs p-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none">
                                <option value="">Select Day</option>
                                <template x-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']">
                                    <option :value="day" x-text="day"></option>
                                </template>
                            </select>"""
    
    form_new = """                            <div class="flex flex-col gap-2">
                                <label class="text-[9px] font-bold text-gray-400 uppercase">Specific Date (for calendar)</label>
                                <input type="date" x-model="newSchedule.date" class="w-full text-xs p-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none">
                            </div>
                            <div class="flex flex-col gap-2">
                                <label class="text-[9px] font-bold text-gray-400 uppercase">Or Recurring Day</label>
                                <select x-model="newSchedule.day" class="w-full text-xs p-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none">
                                    <option value="">No recurrence</option>
                                    <template x-for="day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Daily']">
                                        <option :value="day" x-text="day"></option>
                                    </template>
                                </select>
                            </div>"""
    
    if form_old in content:
        content = content.replace(form_old, form_new)

    # 3. Update the item display to show the date if present
    item_display_old = """                                                    <div class="text-[10px] text-gray-500" x-text="item.time"></div>"""
    
    item_display_new = """                                                    <div class="text-[10px] text-gray-500">
                                                        <span x-show="item.date" x-text="item.date + ' • '"></span>
                                                        <span x-text="item.time"></span>
                                                    </div>"""
    
    if item_display_old in content:
        content = content.replace(item_display_old, item_display_new)

    # 4. Filter schedule items to show relevant ones in the main list
    # The current list shows by Day. I'll also add a "Upcoming Dated Activities" group.
    
    dated_group_top = """                    <!-- Schedule List -->
                    <div x-show="!isScheduling" class="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                        <!-- Dated Items -->
                        <div x-show="scheduleItems.some(i => i.date)" class="mb-4">
                            <div class="font-bold text-[10px] uppercase tracking-wider text-red-500 mb-2">📅 TRACKED DATES</div>
                            <div class="space-y-2">
                                <template x-for="item in scheduleItems.filter(i => i.date).sort((a,b) => new Date(a.date) - new Date(b.date))" :key="item.id">
                                    <div class="flex items-center justify-between p-3 border-2 border-red-50 rounded-xl hover:border-red-200 transition-all group/item bg-red-50/20">
                                        <div class="flex items-center gap-3">
                                            <div class="w-2 h-8 rounded-full bg-red-500"></div>
                                            <div>
                                                <div class="text-xs font-bold text-gray-900" x-text="item.activity"></div>
                                                <div class="text-[10px] text-red-600 font-bold" x-text="new Date(item.date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) + ' @ ' + item.time"></div>
                                            </div>
                                        </div>
                                        <button @click="deleteSchedule(item.id)" class="opacity-0 group-hover/item:opacity-100 p-1.5 hover:bg-red-50 text-gray-400 hover:text-red-700 rounded-lg transition-all">
                                            <i data-lucide="trash-2" class="w-3 h-3"></i>
                                        </button>
                                    </div>
                                </template>
                            </div>
                        </div>"""

    if dated_group_top not in content:
        content = content.replace('<!-- Schedule List -->\n                    <div x-show="!isScheduling" class="space-y-4 max-h-[400px] overflow-y-auto pr-2">', dated_group_top)

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated dashboard.html with date tracking and calendar input")

update_dashboard()
