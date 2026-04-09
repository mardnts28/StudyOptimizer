
import os
import django
import mimetypes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyoptimizer.settings')
django.setup()

from main.models import SharedMaterial

def migrate_to_db():
    materials = SharedMaterial.objects.all()
    print(f"Checking {materials.count()} materials...")
    
    for m in materials:
        if m.file and not m.file_content:
            try:
                print(f"Checking {m.title} ({m.file.name})...")
                # Use Django's open() which works with Cloudinary/S3/Local
                with m.file.open('rb') as f:
                    m.file_content = f.read()
                m.file_mimetype, _ = mimetypes.guess_type(m.file.name)
                m.save()
                print(f"Successfully migrated {m.title} to DB.")
            except Exception as e:
                print(f"Skipping {m.title}: {e}")
        elif m.file_content:
            print(f"Skipping {m.title}: Already in DB.")
        else:
            print(f"Skipping {m.title}: No file attached.")

if __name__ == "__main__":
    migrate_to_db()
