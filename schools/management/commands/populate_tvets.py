"""
Management command to populate Kenyan TVET institutions in the bursary system.
Creates TVETs with default programs and main campus.
"""

from django.core.management.base import BaseCommand
from schools.models import School, SchoolCategory, Campus, Program


class Command(BaseCommand):
    help = 'Populate Kenyan TVET institutions data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating TVET institutions data...'))
        
        # Get or create TVET category
        tvet_category, _ = SchoolCategory.objects.get_or_create(
            name='TVET',
            defaults={'description': 'Technical and Vocational Education and Training Institutions in Kenya'}
        )
        
        # National Polytechnics
        national_polytechnics = [
            'Baringo National Polytechnic',
            'Bumbe National Polytechnic',
            'Bungoma National Polytechnic',
            'Bureti National Polytechnic',
            'Eldoret National Polytechnic',
            'Friends National Polytechnic Kaimosi',
            'Jeremiah Nyagah National Polytechnic',
            'Kabete National Polytechnic',
            'Kaiboi National Polytechnic',
            'Kenya Coast National Polytechnic',
            'Kiambu National Polytechnic',
            'Kisii National Polytechnic',
            'Kisumu National Polytechnic',
            'Kitale National Polytechnic',
            'Maasai National Polytechnic (formerly Masai Technical Training Institute)',
            'Mawego National Polytechnic',
            'Meru National Polytechnic',
            'Morendat Institute of Oil and Gas National Polytechnic',
            'Nairobi National Polytechnic',
            'North Eastern National Polytechnic',
            'Nyandarua National Polytechnic',
            'Nyeri National Polytechnic',
            'Siaya National Polytechnic',
            'Sigalagala National Polytechnic',
            'Shamberere National Polytechnic',
        ]
        
        # Teachers Training Colleges
        teachers_colleges = [
            'Asumbi Teachers Training College',
            'Bishop Mahon Teachers Training College',
            'Bunyore Teachers Training College',
            'Galana Teachers Training College',
            'Garissa Teachers Training College',
            'Kagumo Teachers Training College',
            'Kaimosi Teachers Training College',
            'Kericho Teachers Training College',
            'Kibabii Diploma Teachers Training College',
            'Kitui Teachers Training College',
            'Kwale Teachers Training College',
            'Lugari Teachers Training College',
            'Meru Teachers Training College',
            'Narok Teachers Training College',
            'Rachuonyo Teachers Training College',
            'Seme Teachers Training College',
            "St. Augustine Teacher's Training College - Eregi",
            'Tambach Teachers Training College',
            'Vantage Teachers Training College',
        ]
        
        # Combine all TVETs
        all_tvets = national_polytechnics + teachers_colleges
        
        created_count = 0
        skipped_count = 0
        
        for index, tvet_name in enumerate(all_tvets, start=1):
            # Auto-detect location from TVET name or set as Kenya
            location = 'Kenya'
            if 'Nairobi' in tvet_name:
                location = 'Nairobi'
            elif 'Mombasa' in tvet_name or 'Coast' in tvet_name:
                location = 'Mombasa'
            elif 'Kisumu' in tvet_name:
                location = 'Kisumu'
            elif 'Eldoret' in tvet_name:
                location = 'Eldoret'
            elif 'Kitale' in tvet_name:
                location = 'Kitale'
            elif 'Baringo' in tvet_name:
                location = 'Kabarnet'
            elif 'Bungoma' in tvet_name or 'Bumbe' in tvet_name:
                location = 'Bungoma'
            elif 'Bureti' in tvet_name or 'Kericho' in tvet_name:
                location = 'Kericho'
            elif 'Kaimosi' in tvet_name or 'Friends' in tvet_name:
                location = 'Kaimosi'
            elif 'Kabete' in tvet_name:
                location = 'Kabete'
            elif 'Kiambu' in tvet_name:
                location = 'Kiambu'
            elif 'Kisii' in tvet_name:
                location = 'Kisii'
            elif 'Maasai' in tvet_name or 'Masai' in tvet_name or 'Narok' in tvet_name:
                location = 'Narok'
            elif 'Meru' in tvet_name:
                location = 'Meru'
            elif 'Nyandarua' in tvet_name:
                location = 'Ol Kalou'
            elif 'Nyeri' in tvet_name:
                location = 'Nyeri'
            elif 'Siaya' in tvet_name or 'Asumbi' in tvet_name or 'Seme' in tvet_name:
                location = 'Siaya'
            elif 'Sigalagala' in tvet_name or 'Kakamega' in tvet_name or 'Bunyore' in tvet_name or 'Lugari' in tvet_name:
                location = 'Kakamega'
            elif 'Garissa' in tvet_name or 'North Eastern' in tvet_name:
                location = 'Garissa'
            elif 'Kagumo' in tvet_name:
                location = 'Kagumo'
            elif 'Kibabii' in tvet_name:
                location = 'Bungoma'
            elif 'Kitui' in tvet_name:
                location = 'Kitui'
            elif 'Kwale' in tvet_name:
                location = 'Kwale'
            elif 'Rachuonyo' in tvet_name:
                location = 'Rachuonyo'
            elif 'Eregi' in tvet_name:
                location = 'Eregi'
            elif 'Tambach' in tvet_name:
                location = 'Tambach'
            
            # Generate unique code
            words = tvet_name.replace('(', '').replace(')', '').replace("'", '').split()
            code_prefix = ''.join([word[0].upper() for word in words[:3] if word[0].isalpha()])[:6]
            code = f"TVET{code_prefix}{index:03d}"
            
            # Check if TVET already exists
            school, created = School.objects.get_or_create(
                name=tvet_name,
                defaults={
                    'category': tvet_category,
                    'location': location,
                    'code': code,
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created TVET: {tvet_name}')
                )
                
                # Create main campus
                Campus.objects.get_or_create(
                    school=school,
                    name='Main Campus',
                    defaults={
                        'location': location,
                        'city': location,
                        'is_main_campus': True,
                        'is_active': True,
                    }
                )
                
                # Create default program - use Certificate for TVETs
                Program.objects.get_or_create(
                    school=school,
                    name='General Studies',
                    defaults={
                        'level': 'Certificate',
                        'duration_months': 12,
                        'description': 'Default program for bursary application',
                        'is_active': True,
                    }
                )
                
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⊘ TVET already exists: {tvet_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Completed! Created {created_count} TVETs, skipped {skipped_count} existing TVETs.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total TVETs in database: {School.objects.filter(category=tvet_category).count()}')
        )
