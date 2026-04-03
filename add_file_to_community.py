import os
import re

models_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\models.py'

def update_shared_material_model():
    with open(models_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add file field to SharedMaterial
    old_fields = """    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_materials', blank=True)"""
    
    new_fields = """    content = models.TextField()
    file = models.FileField(upload_to='shared_files/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_materials', blank=True)"""
    
    if old_fields in content:
        content = content.replace(old_fields, new_fields)
    
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added file field to SharedMaterial model")

update_shared_material_model()
