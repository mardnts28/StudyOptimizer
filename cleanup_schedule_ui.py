import os
import re

dashboard_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\dashboard.html'

def update_dashboard_schedule():
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update form in the Modal
    # Remove "Or Recurring Day" div and update "time" input to be structured
    
    # Let's find the grid that contains these
    form_old = """<div class="grid grid-cols-2 gap-3">
                            <div class="flex flex-col gap-2">
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
                            </div>
                            <input type="text" x-model="newSchedule.time" placeholder="e.g. 9:00 AM" class="w-full text-xs p-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none">
                        </div>"""

    form_new = """<div class="grid grid-cols-1 gap-4">
                            <div class="flex flex-col gap-2">
                                <label class="text-[9px] font-bold text-gray-400 uppercase tracking-widest">Select Date 📅</label>
                                <input type="date" x-model="newSchedule.date" class="w-full text-sm p-3 bg-white border-2 border-gray-100 rounded-xl focus:border-red-400 outline-none transition-all">
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <label class="text-[9px] font-bold text-gray-400 uppercase tracking-widest">Set Time ⏰</label>
                                <div class="flex gap-2">
                                    <input type="number" x-model="timeInputs.hour" placeholder="HH" min="1" max="12" class="w-16 p-3 bg-white border-2 border-gray-100 rounded-xl focus:border-red-400 outline-none text-center">
                                    <span class="flex items-center font-bold text-gray-300">:</span>
                                    <input type="number" x-model="timeInputs.minute" placeholder="MM" min="0" max="59" class="w-16 p-3 bg-white border-2 border-gray-100 rounded-xl focus:border-red-400 outline-none text-center">
                                    <select x-model="timeInputs.ampm" class="flex-1 p-3 bg-red-50 border-2 border-red-100 rounded-xl font-bold text-red-700 outline-none">
                                        <option value="AM">AM</option>
                                        <option value="PM">PM</option>
                                    </select>
                                </div>
                            </div>
                        </div>"""

    # Robust replacement
    content = re.sub(r'<div class="grid grid-cols-2 gap-3">.*?<input type="text" x-model="newSchedule\.time".*?</div>', form_new, content, flags=re.DOTALL)

    # 2. Update Alpine.js State and saveSchedule function
    state_old = "newSchedule: { day: '', date: '', time: '', activity: '', color: 'blue' },"
    state_new = """newSchedule: { day: 'General', date: '', time: '', activity: '', color: 'blue' },
                timeInputs: { hour: '09', minute: '00', ampm: 'AM' },"""
    
    if state_old in content:
        content = content.replace(state_old, state_new)
    
    # Handle the time combination in saveSchedule
    save_old = "if (this.newSchedule.day && this.newSchedule.time && this.newSchedule.activity)"
    save_new = """// Combine time components
                    this.newSchedule.time = `${this.timeInputs.hour}:${this.timeInputs.minute.toString().padStart(2, '0')} ${this.timeInputs.ampm}`;
                    if (this.newSchedule.activity)"""
    
    if save_old in content:
        content = content.replace(save_old, save_new)

    # 3. Update the container header name to be more accurate
    header_old = "📅 TRACKED DATES"
    header_new = "🗓️ UPCOMING STUDY SESSIONS"
    if header_old in content:
        content = content.replace(header_old, header_new)

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned up dashboard schedule UI: removed recurring days and added structured AM/PM time input.")

update_dashboard_schedule()
