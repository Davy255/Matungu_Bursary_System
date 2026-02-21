from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile


class Command(BaseCommand):
    help = 'Add National IDs to existing users for fraud prevention'

    def add_arguments(self, parser):
        parser.add_argument(
            'data',
            type=str,
            help='User data in format: username:national_id,username:national_id'
        )

    def handle(self, *args, **options):
        data = options['data']
        users_data = data.split(',')
        
        updated_count = 0
        failed_count = 0
        errors = []
        
        self.stdout.write(self.style.SUCCESS(f'Processing {len(users_data)} users...'))
        
        for user_data in users_data:
            try:
                username, national_id = user_data.split(':')
                username = username.strip()
                national_id = national_id.strip()
                
                # Get user
                user = User.objects.get(username=username)
                
                # Get or create profile
                profile, created = UserProfile.objects.get_or_create(user=user)
                
                # Update national ID
                profile.national_id = national_id
                profile.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Updated {username} with National ID: {national_id}'
                    )
                )
                updated_count += 1
                
            except User.DoesNotExist:
                failed_count += 1
                error_msg = f'User "{username}" not found'
                self.stdout.write(self.style.ERROR(f'✗ {error_msg}'))
                errors.append(error_msg)
            except ValueError:
                failed_count += 1
                error_msg = f'Invalid format in "{user_data}". Use: username:national_id'
                self.stdout.write(self.style.ERROR(f'✗ {error_msg}'))
                errors.append(error_msg)
            except Exception as e:
                failed_count += 1
                error_msg = f'Error updating {username}: {str(e)}'
                self.stdout.write(self.style.ERROR(f'✗ {error_msg}'))
                errors.append(error_msg)
        
        # Print summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated: {updated_count}'))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f'Failed: {failed_count}'))
        self.stdout.write('='*60)
        
        if not errors:
            self.stdout.write(self.style.SUCCESS('All National IDs added successfully!'))
