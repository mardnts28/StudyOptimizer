import os

views_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\views.py'

def update_views_json():
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update collaborate view loop
    old_item = """            'tags':          [m.subject],
        })"""
    new_item = """            'tags':          [m.subject],
            'file_url':      m.file.url if m.file else None,
        })"""
    
    if old_item in content:
        content = content.replace(old_item, new_item)

    # 2. Update share_material response
    old_share_resp = """            'emoji':         material.emoji,
            'liked':         False,
            'tags':          [material.subject],
        }})"""
    
    new_share_resp = """            'emoji':         material.emoji,
            'liked':         False,
            'tags':          [material.subject],
            'file_url':      material.file.url if material.file else None,
        }})"""
        
    if old_share_resp in content:
        content = content.replace(old_share_resp, new_share_resp)

    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated JSON responses to include file URLs")

update_views_json()
