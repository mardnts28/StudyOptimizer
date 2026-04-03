import os

models_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\models.py'

def fix_models():
    with open(models_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Correct the syntax error
    content = content.replace('f"{self.date if self.date else self.day}: {self.activity}" "', 'f"{self.date if self.date else self.day}: {self.activity}"')
    
    with open(models_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed syntax error in models.py")

fix_models()
