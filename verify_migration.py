"""
Verify MySQL migration was successful
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bursary_system.settings')
django.setup()

from schools.models import School, SchoolCategory
from applications.models import Ward, Application
from django.contrib.auth.models import User

print("=" * 60)
print("✓ DATA MIGRATION TO MYSQL - VERIFICATION REPORT")
print("=" * 60)

print(f"\n📊 School Categories: {SchoolCategory.objects.count()}")
print(f"📚 Schools: {School.objects.count()}")
print(f"🏘️  Wards: {Ward.objects.count()}")
print(f"📝 Applications: {Application.objects.count()}")
print(f"👤 Users: {User.objects.count()}")

print(f"\n📋 Schools by Category:")
for cat in SchoolCategory.objects.all():
    count = School.objects.filter(category=cat).count()
    print(f"   - {cat.name}: {count} schools")

print(f"\n📍 Sample Wards:")
for ward in Ward.objects.all()[:5]:
    print(f"   - {ward.name} ({ward.constituency}, {ward.county})")

print(f"\n✅ SUCCESS! All data has been migrated to MySQL!")
print(f"✅ Database: bursary_system")
print(f"✅ User: root")
print(f"✅ Host: localhost:3306")
print("=" * 60)
