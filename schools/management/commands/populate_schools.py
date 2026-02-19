from django.core.management.base import BaseCommand
from schools.models import SchoolCategory, School, Program, Campus


class Command(BaseCommand):
    help = 'Populate initial school categories and sample schools'

    def handle(self, *args, **options):
        # Create school categories
        categories_data = [
            {
                'name': 'University',
                'description': 'Public and private universities in Kenya'
            },
            {
                'name': 'College',
                'description': 'Middle-level and tertiary colleges'
            },
            {
                'name': 'TVET',
                'description': 'Technical and Vocational Education and Training institutions'
            },
        ]
        
        for cat_data in categories_data:
            category, created = SchoolCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        
        # Create sample universities
        universities = [
            {
                'name': 'University of Nairobi',
                'category': 'University',
                'location': 'Nairobi',
                'code': 'UON001'
            },
            {
                'name': 'Kenyatta University',
                'category': 'University',
                'location': 'Nairobi',
                'code': 'KU001'
            },
            {
                'name': 'Maseno University',
                'category': 'University',
                'location': 'Kisumu',
                'code': 'MU001'
            },
        ]
        
        for school_data in universities:
            category = SchoolCategory.objects.get(name=school_data['category'])
            school, created = School.objects.get_or_create(
                name=school_data['name'],
                defaults={
                    'category': category,
                    'location': school_data['location'],
                    'code': school_data['code'],
                    'county': 'Kakamega'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created school: {school.name}'))

            Campus.objects.get_or_create(
                school=school,
                name='Main Campus',
                defaults={
                    'location': school.location or 'Main Campus',
                    'city': school.location or 'Main Campus',
                    'is_main_campus': True
                }
            )

            Program.objects.get_or_create(
                school=school,
                name='Computer Science',
                defaults={'level': 'Degree', 'duration_months': 48}
            )
            Program.objects.get_or_create(
                school=school,
                name='Business Administration',
                defaults={'level': 'Degree', 'duration_months': 48}
            )
            Program.objects.get_or_create(
                school=school,
                name='Education Arts',
                defaults={'level': 'Degree', 'duration_months': 48}
            )
        
        # Create sample colleges
        colleges = [
            {
                'name': 'KMTC Kakamega',
                'category': 'College',
                'location': 'Kakamega',
                'code': 'KMTC001'
            },
            {
                'name': 'Muranga Teachers College',
                'category': 'College',
                'location': 'Murang\'a',
                'code': 'MTC001'
            },
        ]
        
        for school_data in colleges:
            category = SchoolCategory.objects.get(name=school_data['category'])
            school, created = School.objects.get_or_create(
                name=school_data['name'],
                defaults={
                    'category': category,
                    'location': school_data['location'],
                    'code': school_data['code'],
                    'county': 'Kakamega'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created school: {school.name}'))

            Campus.objects.get_or_create(
                school=school,
                name='Main Campus',
                defaults={
                    'location': school.location or 'Main Campus',
                    'city': school.location or 'Main Campus',
                    'is_main_campus': True
                }
            )

            Program.objects.get_or_create(
                school=school,
                name='Accounting',
                defaults={'level': 'Diploma', 'duration_months': 24}
            )
            Program.objects.get_or_create(
                school=school,
                name='Nursing',
                defaults={'level': 'Diploma', 'duration_months': 36}
            )
            Program.objects.get_or_create(
                school=school,
                name='Information Technology',
                defaults={'level': 'Diploma', 'duration_months': 24}
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))
