"""
Extract only important models from backup
"""
import json

print("Loading backup data...")
with open('data_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total records: {len(data)}")

# Models to keep (skip user profiles and other problematic models)
keep_models = [
    'schools.schoolcategory',
    'schools.school',
    'schools.campus',
    'schools.program',
    'applications.ward',
    'applications.application',
    'applications.applicationdocument',
    'applications.applicationreview',
    'applications.applicationcomment',
    'applications.applicationapproval',
    'auth.user',
]

filtered_data = []
model_summary = {}

for item in data:
    model = item.get('model')
    if model in keep_models:
        filtered_data.append(item)
        model_summary[model] = model_summary.get(model, 0) + 1

print(f"\nFiltered records: {len(filtered_data)}")
print("\nRecords by model:")
for model, count in sorted(model_summary.items()):
    print(f"  {model}: {count}")

# Save filtered data
print("\nSaving filtered backup...")
with open('data_backup_clean.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=2, ensure_ascii=False)

print("✓ Clean backup saved to data_backup_clean.json")
