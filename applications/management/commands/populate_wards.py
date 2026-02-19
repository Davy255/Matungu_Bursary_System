"""
Management command to populate wards data for the bursary application system.
This includes sample wards from various constituencies and counties in Kenya.
"""

from django.core.management.base import BaseCommand
from applications.models import Ward


class Command(BaseCommand):
    help = 'Populate wards data for applicant location tracking'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating wards data...'))
        
        # Sample wards data from various counties in Kenya
        # Format: (name, constituency, county)
        wards_data = [
            # Nairobi County
            ('Imara Daima', 'Embakasi South', 'Nairobi'),
            ('Kwa Njenga', 'Embakasi South', 'Nairobi'),
            ('Kwa Reuben', 'Embakasi South', 'Nairobi'),
            ('Pipeline', 'Embakasi South', 'Nairobi'),
            ('Kware', 'Embakasi South', 'Nairobi'),
            
            ('Kayole North', 'Embakasi North', 'Nairobi'),
            ('Kayole Central', 'Embakasi North', 'Nairobi'),
            ('Kayole South', 'Embakasi North', 'Nairobi'),
            ('Komarock', 'Embakasi North', 'Nairobi'),
            ('Matopeni/Spring Valley', 'Embakasi North', 'Nairobi'),
            
            ('Upper Savannah', 'Embakasi Central', 'Nairobi'),
            ('Lower Savannah', 'Embakasi Central', 'Nairobi'),
            ('Embakasi', 'Embakasi Central', 'Nairobi'),
            ('Utawala', 'Embakasi Central', 'Nairobi'),
            ('Mihango', 'Embakasi Central', 'Nairobi'),
            
            ('Umoja I', 'Embakasi East', 'Nairobi'),
            ('Umoja II', 'Embakasi East', 'Nairobi'),
            ('Mowlem', 'Embakasi East', 'Nairobi'),
            ('Kariobangi North', 'Embakasi East', 'Nairobi'),
            
            ('Dandora Area I', 'Embakasi West', 'Nairobi'),
            ('Dandora Area II', 'Embakasi West', 'Nairobi'),
            ('Dandora Area III', 'Embakasi West', 'Nairobi'),
            ('Dandora Area IV', 'Embakasi West', 'Nairobi'),
            
            ('Karen', 'Lang\'ata', 'Nairobi'),
            ('Nairobi West', 'Lang\'ata', 'Nairobi'),
            ('Mugumo-ini', 'Lang\'ata', 'Nairobi'),
            ('South C', 'Lang\'ata', 'Nairobi'),
            ('Nyayo Highrise', 'Lang\'ata', 'Nairobi'),
            
            ('Kibra', 'Kibra', 'Nairobi'),
            ('Laini Saba', 'Kibra', 'Nairobi'),
            ('Lindi', 'Kibra', 'Nairobi'),
            ('Makina', 'Kibra', 'Nairobi'),
            ('Woodley/Kenyatta Golf Course', 'Kibra', 'Nairobi'),
            
            ('Kariokor', 'Starehe', 'Nairobi'),
            ('Ngara', 'Starehe', 'Nairobi'),
            ('Landimawe', 'Starehe', 'Nairobi'),
            ('Nairobi Central', 'Starehe', 'Nairobi'),
            ('Pangani', 'Starehe', 'Nairobi'),
            
            ('Ziwani/Kariokor', 'Kamukunji', 'Nairobi'),
            ('Airbase', 'Kamukunji', 'Nairobi'),
            ('California', 'Kamukunji', 'Nairobi'),
            ('Eastleigh North', 'Kamukunji', 'Nairobi'),
            ('Eastleigh South', 'Kamukunji', 'Nairobi'),
            
            ('Parklands/Highridge', 'Westlands', 'Nairobi'),
            ('Karura', 'Westlands', 'Nairobi'),
            ('Kangemi', 'Westlands', 'Nairobi'),
            ('Mountain View', 'Westlands', 'Nairobi'),
            ('Kitisuru', 'Westlands', 'Nairobi'),
            
            # Kiambu County
            ('Ting\'ang\'a', 'Kiambaa', 'Kiambu'),
            ('Ndenderu', 'Kiambaa', 'Kiambu'),
            ('Muchatha', 'Kiambaa', 'Kiambu'),
            ('Kihara', 'Kiambaa', 'Kiambu'),
            ('Cianda', 'Kiambaa', 'Kiambu'),
            
            ('Biashara', 'Kikuyu', 'Kiambu'),
            ('Karai', 'Kikuyu', 'Kiambu'),
            ('Nachu', 'Kikuyu', 'Kiambu'),
            ('Sigona', 'Kikuyu', 'Kiambu'),
            ('Kikuyu', 'Kikuyu', 'Kiambu'),
            
            ('Ndeiya', 'Limuru', 'Kiambu'),
            ('Ngecha', 'Limuru', 'Kiambu'),
            ('Limuru Central', 'Limuru', 'Kiambu'),
            ('Limuru East', 'Limuru', 'Kiambu'),
            ('Bibirioni', 'Limuru', 'Kiambu'),
            
            # Machakos County
            ('Kangundo North', 'Kangundo', 'Machakos'),
            ('Kangundo Central', 'Kangundo', 'Machakos'),
            ('Kangundo East', 'Kangundo', 'Machakos'),
            ('Kangundo West', 'Kangundo', 'Machakos'),
            
            ('Tala', 'Matungulu', 'Machakos'),
            ('Matungulu North', 'Matungulu', 'Machakos'),
            ('Matungulu West', 'Matungulu', 'Machakos'),
            ('Matungulu East', 'Matungulu', 'Machakos'),
            ('Kyeleni', 'Matungulu', 'Machakos'),
            
            # Mombasa County
            ('Changamwe', 'Changamwe', 'Mombasa'),
            ('Port Reitz', 'Changamwe', 'Mombasa'),
            ('Kipevu', 'Changamwe', 'Mombasa'),
            ('Airport', 'Changamwe', 'Mombasa'),
            ('Chaani', 'Changamwe', 'Mombasa'),
            
            ('港湾', 'Mvita', 'Mombasa'),
            ('Shimanzi/Ganjoni', 'Mvita', 'Mombasa'),
            ('Majengo', 'Mvita', 'Mombasa'),
            ('Tononoka', 'Mvita', 'Mombasa'),
            
            # Kisumu County
            ('Market Milimani', 'Kisumu Central', 'Kisumu'),
            ('Kondele', 'Kisumu Central', 'Kisumu'),
            ('Nyalenda A', 'Kisumu Central', 'Kisumu'),
            ('Nyalenda B', 'Kisumu Central', 'Kisumu'),
            
            ('Manyatta B', 'Kisumu East', 'Kisumu'),
            ('Migosi', 'Kisumu East', 'Kisumu'),
            ('Nyalenda A', 'Kisumu East', 'Kisumu'),
            ('Kajulu', 'Kisumu East', 'Kisumu'),
            
            # Nakuru County
            ('Menengai West', 'Nakuru Town West', 'Nakuru'),
            ('Flamingo', 'Nakuru Town West', 'Nakuru'),
            ('Shaabab', 'Nakuru Town West', 'Nakuru'),
            ('Kaptembwo', 'Nakuru Town West', 'Nakuru'),
            
            ('Nakuru East', 'Nakuru Town East', 'Nakuru'),
            ('Biashara', 'Nakuru Town East', 'Nakuru'),
            ('Kivumbini', 'Nakuru Town East', 'Nakuru'),
            ('Flamingo', 'Nakuru Town East', 'Nakuru'),
            
            # Uasin Gishu County
            ('Kimumu', 'Ainabkoi', 'Uasin Gishu'),
            ('Kaptagat', 'Ainabkoi', 'Uasin Gishu'),
            ('Ainabkoi/Olare', 'Ainabkoi', 'Uasin Gishu'),
            
            ('Simat/Kapseret', 'Kapseret', 'Uasin Gishu'),
            ('Kipkenyo', 'Kapseret', 'Uasin Gishu'),
            ('Ngeria', 'Kapseret', 'Uasin Gishu'),
            ('Megun', 'Kapseret', 'Uasin Gishu'),
            
            # Kakamega County
            ('Butsotso East', 'Lurambi', 'Kakamega'),
            ('Butsotso South', 'Lurambi', 'Kakamega'),
            ('Butsotso Central', 'Lurambi', 'Kakamega'),
            ('Sheywe', 'Lurambi', 'Kakamega'),
            
            ('Mahiakalo', 'Ikolomani', 'Kakamega'),
            ('Idakho South', 'Ikolomani', 'Kakamega'),
            ('Idakho East', 'Ikolomani', 'Kakamega'),
            ('Idakho North', 'Ikolomani', 'Kakamega'),
            
            ('Khalaba_', 'Matungu', 'Kakamega'),
            ('Kholera', 'Matungu', 'Kakamega'),
            ('Mayoni', 'Matungu', 'Kakamega'),
            ('Namamali', 'Matungu', 'Kakamega'),
            ('Koyonzo', 'Matungu', 'Kakamega'),
            
            # Bungoma County
            ('Kanduyi', 'Kanduyi', 'Bungoma'),
            ('Musikoma', 'Kanduyi', 'Bungoma'),
            ('East Sang\'alo', 'Kanduyi', 'Bungoma'),
            ('Bukembe West', 'Kanduyi', 'Bungoma'),
            
            ('Khalaba', 'Webuye East', 'Bungoma'),
            ('Maraka', 'Webuye East', 'Bungoma'),
            ('Mihuu', 'Webuye East', 'Bungoma'),
            ('Ndivisi', 'Webuye East', 'Bungoma'),
            
            # Nyeri County
            ('Ruring\'u', 'Nyeri Town', 'Nyeri'),
            ('Gatitu/Muruguru', 'Nyeri Town', 'Nyeri'),
            ('Rware', 'Nyeri Town', 'Nyeri'),
            ('Kamakwa/Mukaro', 'Nyeri Town', 'Nyeri'),
            
            # Murang\'a County
            ('Gaturi', 'Kigumo', 'Murang\'a'),
            ('Kigumo', 'Kigumo', 'Murang\'a'),
            ('Kahumbu', 'Kigumo', 'Murang\'a'),
            ('Muthithi', 'Kigumo', 'Murang\'a'),
            
            # Meru County
            ('Abothuguchi Central', 'Central Imenti', 'Meru'),
            ('Abothuguchi West', 'Central Imenti', 'Meru'),
            ('Kiagu', 'Central Imenti', 'Meru'),
            ('Mitunguu', 'Central Imenti', 'Meru'),
            
            # Embu County
            ('Gaturi South', 'Manyatta', 'Embu'),
            ('Kithimu', 'Manyatta', 'Embu'),
            ('Kirimari', 'Manyatta', 'Embu'),
            ('Ruguru/Ngandori', 'Manyatta', 'Embu'),
        ]
        
        created_count = 0
        skipped_count = 0
        
        for ward_name, constituency, county in wards_data:
            ward, created = Ward.objects.get_or_create(
                name=ward_name,
                defaults={
                    'constituency': constituency,
                    'county': county,
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created ward: {ward_name} ({constituency}, {county})')
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⊘ Ward already exists: {ward_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Completed! Created {created_count} wards, skipped {skipped_count} existing wards.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total wards in database: {Ward.objects.count()}')
        )
