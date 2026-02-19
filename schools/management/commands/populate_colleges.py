"""
Management command to populate Kenyan colleges in the bursary system.
Creates colleges with default programs and main campus.
"""

from django.core.management.base import BaseCommand
from schools.models import School, SchoolCategory, Campus, Program


class Command(BaseCommand):
    help = 'Populate Kenyan colleges data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating colleges data...'))
        
        # Get or create College category
        college_category, _ = SchoolCategory.objects.get_or_create(
            name='College',
            defaults={'description': 'Technical, Vocational, and Professional Colleges in Kenya'}
        )
        
        # Technical and Vocational Colleges/Training Institutes
        technical_colleges = [
            'Ahmed Shahame Mwidani Technical and Vocational College',
            'Aldai Technical Training Institute',
            'Alupe University TVET Institute',
            'Bahati Institute of Business and Administration',
            'Balambala Technical & Vocational College',
            'Bandari Maritime Academy',
            'Belgut Technical and Vocational College',
            'Bomet Central Technical and Vocational College',
            'Bondo Technical Training Institute',
            'Borabu Technical Training Institute',
            'Bukura Agricultural College',
            'Bungoma North Technical and Vocational College',
            'Bunyala Technical Training Institute',
            'Bureti Technical Training Institute',
            'Bushiangala Technical Training Institute',
            'Butere Technical and Vocational College',
            'Butula Technical and Vocational College',
            'Cardinal Maurice Otunga Technical and Vocational College',
            'Centre for Tourism Training and Research',
            'Chamasiri Technical And Vocational College',
            'Chanzeywe Technical and Vocational College',
            'Chepalungu Technical Training Institute',
            'Cherangany Technical and Vocational College',
            'Chepsirei Technical and Vocational College',
            'Chevaywa Technical and Vocational College',
            'Chuka Technical and Vocational College',
            'Chuka University TVET- Igembe Campus',
            'Coast Institute of Technology',
            'Co-operative University of Kenya (CUK) Nairobi CBD Training Institute',
            'David M Wambuli Technical and Vocational College',
            'East Africa Institute of Certified Studies',
            'East Africa School of Aviation',
            'Ebukanga Technical and Vocational College',
            'Ekerubo Gietai Technical Training Institute',
            'Elwak Technical and Vocational College',
            'Emining Technical Training Institute',
            'Emsos Technical And Vocational College',
            'Endebess Technical Training Institute',
            'Fayya Technical and Vocational College',
            'Garissa University TVET Institute',
            'Gatanga Technical and Vocational College',
            'Gatundu South Technical and Vocational College',
            'Gilgil Technical and Vocational College',
            'Githunguri Technical and Vocational College',
            'Gitwebe Technical Training Institute',
            'Godoma Technical Training Institute',
            'Got Ramogi Technical and Vocational College',
            'Ijara Technical and Vocational College',
            'Ikutha Technical Training Institute',
            'Jomo Kenyatta University of Agriculture and Technology TVET Institute',
            'Kabarak University TVET Institute',
            'Kaelo Technical Training Institute',
            'Kajiado West Technical and Vocational College',
            'Kakrao Technical and Vocational College',
            'Kaloleni Technical and Vocational College',
            'Kamukunji Technical and Vocational College',
            'Kapchepkor Technical Training Institute',
            'Kapcherop Technical and Vocational College',
            'Karen Technical Training Institute for the Deaf',
            'Karumo Technical Training Institute',
            'Kasarani Technical and Vocational College',
            'KASNEB',
            'Katine Technical Training Institute',
            'Kendege Technical and Vocational College',
            'Kenya Forestry College',
            'Kenya Industrial Training Institute',
            'Kenya Institute of Highways & Building Technology',
            'Kenya Institute of Mass Communication',
            'Kenya Institute of Surveying and Mapping',
            'Kenya Medical Training College',
            'Kenya School of Agriculture - Songa Mbele Campus',
            'Kenya School of Law',
            'Kenya School of Monetary Studies',
            'Kenya School of Revenue Administration',
            'Kenya School of TVET (formerly Kenya Technical Trainers College)',
            'Kenya Utalii College',
            'Kenya Water Institute',
            'Kenya Wildlife Service Training Institute (now Wildlife Research and Training Institute)',
            'Kenyatta University - City Campus TVET Centre',
            'Kericho Township Technical and Vocational College',
            'Keroka Technical Training Institute',
            'Kibabii University Directorate of TVET College',
            'Kibwezi West Technical and Vocational College',
            'Kieni Technical and Vocational College',
            'Kigumo Technical Training Institute',
            'Kiharu Technical and Vocational College',
            'Kiirua Technical Training Institute',
            'Kilgoris Technical and Vocational College',
            'Kimasian Technical and Vocational College',
            'Kiminini Technical And Vocational College',
            'Kinango Technical And Vocational College',
            'Kinangop Technical And Vocational College',
            'Kinoo Vocational Training Centre',
            'Kipipiri Technical and Vocational College',
            'Kipkabus Technical and Vocational College',
            'Kipsinende Technical and Vocational College',
            'Kipsoen Technical And Vocational College',
            'Kiptaragon Technical And Vocational College',
            'Kirinyaga Central Technical and Vocational College',
            'Kisii University TVET Institute',
            'Kisiwa Technical Training Institute',
            'Kitelakapel Technical and Vocational College',
            'Kitui East Technical and Vocational College',
            'Kitui Rural Technical and Vocational College',
            'Kitutu Chache Technical and Vocational College',
            'Kongoni Technical and Vocational College',
            'Konoin Technical Training Institute',
            'Koshin Technical Training Institute',
            'Khwisero Technical and Vocational College',
            'Lagdera Technical and Vocational College',
            'Laikipia East Technical and Vocational College',
            'Laikipia North Technical and Vocational College',
            'Laikipia West Technical and Vocational College',
            'Laikipia University TVET Institute',
            'Laisamis Technical and Vocational College',
            'Lamu East Technical and Vocational College',
            'Langata Technical and Vocational College',
            'Lari Technical and Vocational College',
            'Limuru Technical Vocational College',
            'Lodwar Technical And Vocational College',
            'Loima Technical and Vocational College',
            'Lungalunga Technical Vocational College',
            'Maasai Mara Technical and Vocational Training College',
            'Maasai Mara University TVET Institute',
            'Mabera Technical and Vocational College',
            'Machakos Technical Institute for the Blind',
            'Machakos Township Technical and Vocational College',
            'Manyatta Technical Vocational College',
            'Marist Technical Vocational College',
            'Masinga Technical and Vocational College',
            'Mathenge Technical Training Institute',
            'Mathioya Technical and Vocational College',
            'Mathira Technical and Vocational College',
            'Matili Technical Training Institute',
            'Mbeere North Technical and Vocational College',
            'Mbita Technical and Vocational College',
            'Merti Technical Training Institute',
            'Meru University of Science and Technology TVET Directorate',
            'Michuki Technical Training Institute',
            'Mitunguu Technical Training Institute',
            'Mochoi Technical and Vocational College',
            'Mochongoi Technical and Vocational College',
            'Moi University TVET Institute',
            'Moiben Technical and Vocational College',
            'Molo Technical and Vocational College',
            'Morendat Institute of Oil & Gas',
            'Msambweni Technical and Vocational College',
            'Mukiria Technical Training Institute',
            'Mukurwe-ini Technical Training Institute',
            'Mulango Technical and Vocational College',
            'Mumias West Technical and Vocational College',
            'Mungatsi Technical and Vocational College',
            "Murang'a Technical Training Institute",
            "Murang'a University of Technology TVET Institute",
            'Musakasa Technical Training Institute',
            'Mwala Technical and Vocational College',
            'Mwatate Technical and Vocational College',
            'Mwea Technical and Vocational College',
            'Nachu Technical and Vocational College',
            'Naivasha Technical and Vocational College',
            'Narok South Technical and Vocational College',
            'Ndaragwa Technical and Vocational College',
            'Ndia Technical and Vocational College',
            'Ngeria Technical and Vocational College',
            'Ngong Technical and Vocational College',
            'Njoro Technical Training Institute',
            'Nkabune Technical Training Institute',
            'North Horr Technical and Vocational College',
            'North Rift Technical and Vocational College',
            'Nuu Technical and Vocational College',
            'Nyaga Vocational Training Centre',
            'Nyakach Technical and Vocational College',
            'Nyando Technical Training Institute',
            'Okame Technical Training Institute',
            'Ol Kalou Technical and Vocational College',
            'Omuga Technical and Vocational College',
            'P.C Kinyanjui Technical Training Institute',
            'Rachuonyo Technical and Vocational College',
            'Railway Training Institute',
            'Ramogi Institute of Advanced Techology',
            'Rangwe Technical and Vocational College',
            'Rarieda Technical and Vocational College',
            'Riamo Technical and Vocational College',
            'Riatirimba Technical and Vocational College',
            'Rift Valley Institute of Science and Technology',
            'Rift Valley Technical Training Institute',
            'Rongo University Technical and Vocational Training Institute',
            'Ruiru Technical and Vocational College',
            'Runyenjes Technical and Vocational College',
            'Rwika Technical Institute',
            'Sabatia Technical and Vocational College',
            'Samburu North Technical and Vocational College',
            'Samburu Technical and Vocational College',
            'Seme Technical and Vocational College',
            'Siala Technical Training Institute',
            'Sirisia Technical and Vocational College',
            'Siruti Technical and Vocational College',
            'Sot Technical Training Institute',
            'Sotik Technical Training Institute',
            'South Eastern Kenya University (SEKU) Directorate of TVET',
            "St. Joseph's Technical Institute for the Deaf Nyang'oma",
            'Subukia Technical and Vocational College',
            'Taita Taveta University Institute of TVET',
            'Tarbaj Technical and Vocational College',
            'Technology Development Centre - Athi River',
            'Tetu Technical and Vocational College',
            'Technical University of Kenya (TUK) Directorate of TVET College',
            'Technical University of Mombasa (TUM) TVET Institute',
            'Tharaka Technical and Vocational College',
            'Tharaka University TVET Institute',
            "The Ol'lessos Technical Training Institute",
            'The University of Embu TVET Institute',
            'Thika Technical Training Institute',
            'Thogoto Vocational Training Centre',
            'Tinderet Intergrated Technical & Trainers College',
            'Tom Mboya Labour College',
            'Turkana East Technical and Vocational College',
            'Turkana University College TVET Institute',
            'Ugenya Technical and Vocational College',
            'Ugunja Technical and Vocational College',
            'Uriri Technical and Vocational College',
            'Wajir East Technical and Vocational College',
            'Wajir South Technical and Vocational College',
            'Watamu Technical and Vocational College',
            'Webuye West Technical and Vocational College',
            'Weru Technical and Vocational College',
            'West Mugirango Technical and Vocational College',
            'Wote Technical Training Institute',
            'Wumingu Technical and Vocational College',
            'Ziwa Technical Training Institute',
        ]
        
        # Professional and Other Colleges
        professional_colleges = [
            'African Institute of Research and Development Studies',
            'Beauty Point College',
            'Bishop Locati Technical Training Institute',
            'Bridgeworld College',
            'Cascade Institute of Hospitality',
            'Clastars College',
            'College of Human Resource Management',
            'Embu College',
            'Equip Africa College of Medical and Health Sciences',
            'Equip Africa Institute',
            'Gretsa Institute of Technical and Professional Studies',
            'Hemland College of Professional and Technical Studies',
            'Highlands State Technical College',
            'ICDL Africa Ltd',
            'JFC Munene College',
            'Joan School of Nursing',
            'Jodan College of Technology',
            'KAN College of Professional Studies',
            'KCA Technical College',
            'Kenya Aeronautical College',
            'Kenya Christian Industrial Training Institute',
            'Kenya Institute of Management',
            'Kenya Institute of Social Work and Community Development',
            'Kenya School of Medical Science and Technology',
            'Kenya YMCA College of Agriculture and Technology',
            'KIPS Technical College',
            'Machakos Institute of Technology',
            'Mahanaim Educational Institute (College)',
            'Maseno School of Nursing and Health Sciences',
            'Nairobi Aviation College',
            'Nairobi College of Bread and Confectionery Technology',
            'Nairobi Institute of Technology',
            'Nairobi Technical Training Institute',
            "Nairobi Women's Hospital College",
            'Nakuru Training Institute',
            'Oshwal College',
            'Outspan Medical College',
            'Rift Valley Institute of Business Studies',
            'Sagana Technical Training Institute',
            'Sensei Institute of Technology',
            'SOS Technical Training Institute',
            'Span Institute of Technology',
            "St. Columba's Technical Training College",
            'Stanbridge College',
            'Technical Institute',
            'Traction School of Governance and Business',
            'Transafric Accountancy and Management College',
            'Tropical Institute of Community Health',
            'Uwezo College',
            'Vera Beauty College',
            'VICODEC Technical Training Institute',
            'Vihiga College of Business and Technical Training',
            'Vitech Training Institute',
        ]
        
        # Combine all colleges
        all_colleges = technical_colleges + professional_colleges
        
        created_count = 0
        skipped_count = 0
        
        for index, college_name in enumerate(all_colleges, start=1):
            # Auto-detect location from college name or set as Kenya
            location = 'Kenya'
            if 'Nairobi' in college_name or 'CBD' in college_name:
                location = 'Nairobi'
            elif 'Mombasa' in college_name:
                location = 'Mombasa'
            elif 'Kisumu' in college_name:
                location = 'Kisumu'
            elif 'Nakuru' in college_name:
                location = 'Nakuru'
            elif 'Eldoret' in college_name:
                location = 'Eldoret'
            elif 'Kakamega' in college_name:
                location = 'Kakamega'
            elif 'Machakos' in college_name:
                location = 'Machakos'
            elif 'Meru' in college_name:
                location = 'Meru'
            elif 'Thika' in college_name:
                location = 'Thika'
            elif 'Athi River' in college_name:
                location = 'Athi River'
            
            # Generate unique code
            words = college_name.replace('(', '').replace(')', '').split()
            code_prefix = ''.join([word[0].upper() for word in words[:3] if word[0].isalpha()])[:6]
            code = f"COL{code_prefix}{index:03d}"
            
            # Check if college already exists
            school, created = School.objects.get_or_create(
                name=college_name,
                defaults={
                    'category': college_category,
                    'location': location,
                    'code': code,
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created college: {college_name}')
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
                
                # Create default program
                Program.objects.get_or_create(
                    school=school,
                    name='General Studies',
                    defaults={
                        'level': 'Diploma',
                        'duration_months': 24,
                        'description': 'Default program for bursary application',
                        'is_active': True,
                    }
                )
                
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⊘ College already exists: {college_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Completed! Created {created_count} colleges, skipped {skipped_count} existing colleges.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total colleges in database: {School.objects.filter(category=college_category).count()}')
        )
