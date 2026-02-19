"""
Management command to populate Kenyan universities in the bursary system.
Creates universities with default programs and main campus.
"""

from django.core.management.base import BaseCommand
from schools.models import School, SchoolCategory, Campus, Program


class Command(BaseCommand):
    help = 'Populate Kenyan universities data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating universities data...'))
        
        # Get or create University category
        university_category, _ = SchoolCategory.objects.get_or_create(
            name='University',
            defaults={'description': 'Public and Private Universities in Kenya'}
        )
        
        # Public Universities
        public_universities = [
            ('Chuka University', 'Chuka, Tharaka-Nithi'),
            ('Co-operative University of Kenya (CUK)', 'Nairobi'),
            ('Dedan Kimathi University of Technology (DKUT)', 'Nyeri'),
            ('Egerton University', 'Njoro, Nakuru'),
            ('Garissa University', 'Garissa'),
            ('Jaramogi Oginga Odinga University of Science and Technology', 'Bondo, Siaya'),
            ('Jomo Kenyatta University of Agriculture and Technology (JKUAT)', 'Juja, Kiambu'),
            ('Kabarnet University College', 'Baringo'),
            ('Karatina University', 'Karatina, Nyeri'),
            ('Koitaleel Samoei University College', 'Nandi'),
            ('Kenyatta University (KU)', 'Nairobi'),
            ('Kibabii University (KIBU)', 'Bungoma'),
            ('Kirinyaga University', 'Kirinyaga'),
            ('Kisii University', 'Kisii'),
            ('Laikipia University', 'Nyahururu, Laikipia'),
            ('Maasai Mara University', 'Narok'),
            ('Machakos University', 'Machakos'),
            ('Maseno University', 'Maseno, Kisumu'),
            ('Masinde Muliro University of Science and Technology', 'Kakamega'),
            ('Meru University of Science and Technology', 'Meru'),
            ('Moi University', 'Eldoret, Uasin Gishu'),
            ('Multimedia University of Kenya (MMU)', 'Nairobi'),
            ("Murang'a University of Technology", "Murang'a"),
            ('Nyandarua University College', 'Nyandarua'),
            ('Open University of Kenya (OUK)', 'Nairobi'),
            ('Pwani University', 'Kilifi'),
            ('Rongo University', 'Rongo, Migori'),
            ('South Eastern Kenya University (SEKU)', 'Kitui'),
            ('Taita Taveta University', 'Voi, Taita Taveta'),
            ('Technical University of Kenya (TUK)', 'Nairobi'),
            ('Technical University of Mombasa (TUM)', 'Mombasa'),
            ('University of Eldoret', 'Eldoret, Uasin Gishu'),
            ('University of Embu', 'Embu'),
            ('University of Kabianga', 'Kericho'),
            ('University of Nairobi (UON)', 'Nairobi'),
        ]
        
        # Constituent University Colleges
        constituent_colleges = [
            ('Alupe University College (Moi University)', 'Alupe, Busia'),
            ('Kaimosi Friends University College (Masinde Muliro University)', 'Kaimosi, Vihiga'),
            ('Mama Ngina University College (Kenyatta University)', 'Mombasa'),
            ('Tom Mboya University College (Maseno University)', 'Homa Bay'),
            ('Turkana University College (Masinde Muliro University)', 'Lodwar, Turkana'),
            ('Bomet University College (Moi University)', 'Bomet'),
            ('Tharaka University College (Chuka University)', 'Marimanti, Tharaka-Nithi'),
        ]
        
        # Private Universities
        private_universities = [
            ('Africa International University', 'Nairobi'),
            ('African Leadership University', 'Mauritius/Rwanda'),
            ('Africa Nazarene University', 'Nairobi'),
            ('Amref International University', 'Nairobi'),
            ('Catholic University of Eastern Africa', 'Nairobi'),
            ('Daystar University', 'Nairobi'),
            ('Great Lakes University Of Kisumu', 'Kisumu'),
            ('Gretsa University', 'Thika, Kiambu'),
            ('International Leadership University', 'Nairobi'),
            ('Islamic University of Kenya', 'Kajiado'),
            ('Kabarak University', 'Nakuru'),
            ('KAG East University', 'Nairobi'),
            ('KCA University', 'Nairobi'),
            ('Kenya Highlands University', 'Kericho'),
            ('Kenya Methodist University', 'Meru'),
            ('Kiriri Women\'s University of Science & Technology', 'Nairobi'),
            ('Lukenya University', 'Machakos'),
            ('Marist International University College', 'Nairobi'),
            ('Mount Kenya University', 'Thika, Kiambu'),
            ('Pan Africa Christian University', 'Nairobi'),
            ('Pioneer International University', 'Nairobi'),
            ('Riara University', 'Nairobi'),
            ('Scott Christian University', 'Machakos'),
            ('St Paul\'s University', 'Limuru, Kiambu'),
            ('Tangaza University', 'Nairobi'),
            ('The East Africa University', 'Nairobi'),
            ('The Management University Of Africa', 'Nairobi'),
            ('The Presbyterian University Of East Africa', 'Kikuyu, Kiambu'),
            ('United States International University', 'Nairobi'),
            ('University Of Eastern Africa, Baraton', 'Nandi'),
            ('Uzima University College', 'Kisumu'),
            ('Umma University', 'Kajiado'),
            ('Zetech University', 'Nairobi'),
        ]
        
        # Combine all universities
        all_universities = public_universities + constituent_colleges + private_universities
        
        created_count = 0
        skipped_count = 0
        
        for index, (university_name, location) in enumerate(all_universities, start=1):
            # Generate a unique code from the university name + index
            words = university_name.replace('(', '').replace(')', '').split()
            code_prefix = ''.join([word[0].upper() for word in words[:3] if word[0].isalpha()])[:6]
            code = f"{code_prefix}{index:03d}"  # e.g., "CU001", "DKUT002"
            
            # Check if university already exists
            school, created = School.objects.get_or_create(
                name=university_name,
                defaults={
                    'category': university_category,
                    'location': location,
                    'code': code,
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created university: {university_name}')
                )
                
                # Create main campus
                Campus.objects.get_or_create(
                    school=school,
                    name='Main Campus',
                    defaults={
                        'location': location,
                        'city': location.split(',')[-1].strip() if ',' in location else location,
                        'is_main_campus': True,
                        'is_active': True,
                    }
                )
                
                # Create default program for the university
                Program.objects.get_or_create(
                    school=school,
                    name='General Studies',
                    defaults={
                        'level': 'Degree',
                        'duration_months': 48,
                        'description': 'Default program for bursary application',
                        'is_active': True,
                    }
                )
                
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⊘ University already exists: {university_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Completed! Created {created_count} universities, skipped {skipped_count} existing universities.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total universities in database: {School.objects.filter(category=university_category).count()}')
        )
