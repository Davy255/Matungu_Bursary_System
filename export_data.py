"""
Export data from SQLite with proper UTF-8 encoding
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bursary_system.settings')
django.setup()

from django.core.management import call_command
import codecs

# Export data with UTF-8 encoding
print("Exporting data from SQLite...")
with codecs.open('data_backup.json', 'w', encoding='utf-8') as f:
    call_command(
        'dumpdata',
        '--indent=2',
        '--natural-foreign',
        '--natural-primary',
        '-e', 'contenttypes',
        '-e', 'auth.Permission',
        '-e', 'sessions',
        stdout=f
    )

print("✓ Data exported successfully to data_backup.json")
