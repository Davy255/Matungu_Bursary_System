# Generated migration for making ward field optional for CDF Admin

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_add_national_id_unique_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminrole',
            name='ward',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Mayoni', 'Mayoni'),
                    ('Kholera', 'Kholera'),
                    ('Khalaba', 'Khalaba'),
                    ('Koyonzo', 'Koyonzo'),
                    ('Namamali', 'Namamali')
                ],
                help_text='Required for Ward Admin only. Leave blank for CDF Admin.',
                max_length=50,
                null=True
            ),
        ),
    ]
