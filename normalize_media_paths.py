import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyoptimizer.settings')
django.setup()

from main.models import SharedMaterial, SummarizedDocument

def normalize_paths():
    print("Standardizing SharedMaterial file paths...")
    materials = SharedMaterial.objects.filter(file__icontains='media/')
    count = 0
    for m in materials:
        old_path = m.file.name
        if old_path.startswith('media/'):
            m.file.name = old_path.replace('media/', '', 1)
            m.save()
            count += 1
            print(f"  Fixed: {old_path} -> {m.file.name}")
    
    print(f"Finished. Fixed {count} SharedMaterial records.")

    print("\nStandardizing SummarizedDocument file paths...")
    docs = SummarizedDocument.objects.filter(document_file__icontains='media/')
    doc_count = 0
    for d in docs:
        old_path = d.document_file.name
        if old_path.startswith('media/'):
            d.document_file.name = old_path.replace('media/', '', 1)
            d.save()
            doc_count += 1
            print(f"  Fixed: {old_path} -> {d.document_file.name}")
    
    print(f"Finished. Fixed {doc_count} SummarizedDocument records.")

if __name__ == '__main__':
    normalize_paths()
