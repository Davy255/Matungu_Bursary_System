"""
Fix backup data - Remove duplicates and handle unique constraints
"""
import json
import uuid

print("Loading backup data...")
with open('data_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total records: {len(data)}")

# Track which items to keep
items_to_keep = []
seen_user_profiles = set()  # Track user IDs we've already added
fixed_count = 0

for item in data:
    if item.get('model') == 'users.userprofile':
        fields = item.get('fields', {})
        user_id = fields.get('user')
        
        # Convert to string if it's a list
        user_id_key = str(user_id) if isinstance(user_id, list) else user_id
        
        # Skip duplicate user profiles (keep only first one for each user)
        if user_id_key in seen_user_profiles:
            print(f"  Skipping duplicate UserProfile for user_id {user_id_key}")
            fixed_count += 1
            continue
        
        seen_user_profiles.add(user_id_key)
        
        # Fix empty national_id
        if fields.get('national_id') == '':
            fields['national_id'] = f"TEMP-{str(uuid.uuid4())[:12]}"
            print(f"  Fixed empty national_id for user_id {user_id_key}")
        
        items_to_keep.append(item)
    else:
        items_to_keep.append(item)

print(f"\nRemoved {fixed_count} duplicate/invalid records")
print(f"Total records to load: {len(items_to_keep)}")

# Save fixed data
print("Saving fixed backup...")
with open('data_backup_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(items_to_keep, f, indent=2, ensure_ascii=False)

print("✓ Fixed backup saved to data_backup_fixed.json")
