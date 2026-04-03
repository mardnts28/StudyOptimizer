import os
import re

models_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\models.py'
views_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\views.py'
urls_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\urls.py'

def update_models():
    with open(models_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_model = """class ScheduleItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_items')
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    activity = models.CharField(max_length=255)
    color = models.CharField(max_length=20, default='blue')

    def __str__(self):
        return f"{self.day}: {self.activity} \"""
    
    new_model = """class ScheduleItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_items')
    date = models.DateField(null=True, blank=True)
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    activity = models.CharField(max_length=255)
    color = models.CharField(max_length=20, default='blue')

    def __str__(self):
        return f"{self.date if self.date else self.day}: {self.activity}" """
    
    # Use re to be more robust
    content = re.sub(r'class ScheduleItem\(models\.Model\):.*?def __str__\(self\):.*?return f"\{self\.day\}: \{self\.activity\}"', new_model, content, flags=re.DOTALL)
    
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated models.py with date field in ScheduleItem")

def update_views():
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update profile view to include recent summaries
    profile_view_old = """    context = {
        'user_level':          (completed_tasks // 5) + 1,
        'next_level_progress': int(((completed_tasks % 5) / 5) * 100) if (completed_tasks % 5) != 0 or completed_tasks == 0 else 100,
        'docs_count':          summaries_count,
        'completed_count':     completed_tasks,
        'total_tasks':         total_tasks,
        'completion_rate':     round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0,
        'study_hours':         (completed_tasks * 2) + summaries_count,
    }"""
    
    profile_view_new = """    recent_summaries_list = SummarizedDocument.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'user_level':          (completed_tasks // 5) + 1,
        'next_level_progress': int(((completed_tasks % 5) / 5) * 100) if (completed_tasks % 5) != 0 or completed_tasks == 0 else 100,
        'docs_count':          summaries_count,
        'completed_count':     completed_tasks,
        'total_tasks':         total_tasks,
        'completion_rate':     round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0,
        'study_hours':         (completed_tasks * 2) + summaries_count,
        'recent_summaries':    recent_summaries_list,
    }"""
    
    content = content.replace(profile_view_old, profile_view_new)
    
    # 2. Add delete_schedule view
    delete_view = """
@login_required
@require_POST
def delete_schedule_item(request, item_id):
    try:
        ScheduleItem.objects.get(id=item_id, user=request.user).delete()
        return JsonResponse({'status': 'success'})
    except ScheduleItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
"""
    # Insert it before the end (let's just append or find a good place)
    if 'def delete_schedule_item' not in content:
        content += delete_view
        
    # 3. Update add_schedule_item to handle date
    add_old = """    try:
        data = json.loads(request.body)
        item = ScheduleItem.objects.create(
            user     = request.user,
            day      = data.get('day'),
            time     = data.get('time'),
            activity = data.get('activity'),
            color    = data.get('color', 'blue'),
        )"""
    
    add_new = """    try:
        data = json.loads(request.body)
        item = ScheduleItem.objects.create(
            user     = request.user,
            date     = data.get('date') if data.get('date') else None,
            day      = data.get('day') or 'General',
            time     = data.get('time'),
            activity = data.get('activity'),
            color    = data.get('color', 'blue'),
        )"""
    content = content.replace(add_old, add_new)
    
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated views.py with schedule logic and profile summaries")

def update_urls():
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_urls = """    path('tasks/schedule/add/', views.add_schedule_item, name='add_schedule'),
    path('tasks/schedule/delete/<int:item_id>/', views.delete_schedule_item, name='delete_schedule'),
"""
    if 'tasks/schedule/add/' not in content:
        content = content.replace("path('profile/', views.profile, name='profile'),", new_urls + "    path('profile/', views.profile, name='profile'),")
    
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated urls.py with schedule routes")

update_models()
update_views()
update_urls()
