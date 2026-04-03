import os

views_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\views.py'

def fix_view_response():
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_json = """        return JsonResponse({'status': 'success', 'item': {
            'id': item.id, 'day': item.day,
            'time': item.time, 'activity': item.activity, 'color': item.color,
        }})"""
    
    new_json = """        return JsonResponse({'status': 'success', 'item': {
            'id': item.id, 'day': item.day, 'date': item.date.strftime('%Y-%m-%d') if item.date else None,
            'time': item.time, 'activity': item.activity, 'color': item.color,
        }})"""
    
    if old_json in content:
        content = content.replace(old_json, new_json)
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated add_schedule_item response to include date")

fix_view_response()
