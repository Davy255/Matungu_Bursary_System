from django.core.management.base import BaseCommand
from schools.models import School, Campus, Program
from applications.models import Ward

class Command(BaseCommand):
    help = 'Populate database with sample schools, programs, and wards'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating sample data...')
        
        # Create Wards - Matungu Constituency, Kakamega County
        wards_data = [
            {'name': 'Khalaba', 'sub_county': 'Matungu', 'county': 'Kakamega', 'code': 'KKG-MTG-001'},
            {'name': 'Koyonzo', 'sub_county': 'Matungu', 'county': 'Kakamega', 'code': 'KKG-MTG-002'},
            {'name': 'Mayoni', 'sub_county': 'Matungu', 'county': 'Kakamega', 'code': 'KKG-MTG-003'},
            {'name': 'Kholera', 'sub_county': 'Matungu', 'county': 'Kakamega', 'code': 'KKG-MTG-004'},
            {'name': 'Namamali', 'sub_county': 'Matungu', 'county': 'Kakamega', 'code': 'KKG-MTG-005'},
        ]
        
        for ward_data in wards_data:
            Ward.objects.get_or_create(**ward_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(wards_data)} wards'))
        
        # Create Schools
        schools_data = [
            {
                'name': 'University of Nairobi',
                'school_type': 'university',
                'registration_number': 'UON-001',
                'email': 'info@uonbi.ac.ke',
                'phone_number': '+254-20-4913000',
                'address': 'P.O. Box 30197, Nairobi',
                'county': 'Nairobi',
            },
            {
                'name': 'Masinde Muliro University of Science and Technology',
                'school_type': 'university',
                'registration_number': 'MMUST-001',
                'email': 'info@mmust.ac.ke',
                'phone_number': '+254-56-51724',
                'address': 'P.O. Box 190, Kakamega',
                'county': 'Kakamega',
            },
            {
                'name': 'Kenya Medical Training College',
                'school_type': 'college',
                'registration_number': 'KMTC-001',
                'email': 'info@kmtc.ac.ke',
                'phone_number': '+254-20-272-7900',
                'address': 'P.O. Box 30195, Nairobi',
                'county': 'Nairobi',
            },
        ]
        
        schools_created = 0
        for school_data in schools_data:
            school, created = School.objects.get_or_create(
                registration_number=school_data['registration_number'],
                defaults=school_data
            )
            if created:
                schools_created += 1
                
                # Add main campus
                Campus.objects.get_or_create(
                    school=school,
                    name='Main Campus',
                    defaults={'location': school_data['county'], 'is_main': True}
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {schools_created} schools'))
        
        # Create Programs
        programs_data = [
            {'school_reg': 'UON-001', 'name': 'Bachelor of Science in Computer Science', 'code': 'BSC-CS', 'level': 'degree', 'duration': 4},
            {'school_reg': 'UON-001', 'name': 'Bachelor of Medicine and Bachelor of Surgery', 'code': 'MBCHB', 'level': 'degree', 'duration': 6},
            {'school_reg': 'MMUST-001', 'name': 'Bachelor of Education Science', 'code': 'BED-SCI', 'level': 'degree', 'duration': 4},
            {'school_reg': 'MMUST-001', 'name': 'Diploma in Information Technology', 'code': 'DIP-IT', 'level': 'diploma', 'duration': 2},
            {'school_reg': 'KMTC-001', 'name': 'Diploma in Clinical Medicine', 'code': 'DIP-CM', 'level': 'diploma', 'duration': 3},
            {'school_reg': 'KMTC-001', 'name': 'Certificate in Community Health', 'code': 'CERT-CH', 'level': 'certificate', 'duration': 1},
        ]
        
        programs_created = 0
        for prog_data in programs_data:
            try:
                school = School.objects.get(registration_number=prog_data['school_reg'])
                _, created = Program.objects.get_or_create(
                    school=school,
                    code=prog_data['code'],
                    defaults={
                        'name': prog_data['name'],
                        'level': prog_data['level'],
                        'duration_years': prog_data['duration']
                    }
                )
                if created:
                    programs_created += 1
            except School.DoesNotExist:
                pass
        
        self.stdout.write(self.style.SUCCESS(f'Created {programs_created} programs'))
        self.stdout.write(self.style.SUCCESS('Sample data population complete!'))
