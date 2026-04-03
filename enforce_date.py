import os

dashboard_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\dashboard.html'

def require_date_and_activity():
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add required and check in JS
    old_check = "if (this.newSchedule.activity)"
    new_check = "if (this.newSchedule.date && this.newSchedule.activity)"
    
    content = content.replace(old_check, new_check)
    
    # 2. Add validation hint in UI
    old_btn = '<button @click="saveSchedule"'
    new_btn = '<button @click="if(!newSchedule.date || !newSchedule.activity) { alert(\'Please select both a date and activity name!\'); return; } saveSchedule()"'
    
    content = content.replace(old_btn, new_btn)

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Enforced date selection for study sessions.")

require_date_and_activity()
