# Generated migration for adding verification fields to AdminRole and UserProfile

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_alter_adminrole_ward'),
    ]

    operations = [
        # Add verification fields to AdminRole
        migrations.AddField(
            model_name='adminrole',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='Verified by Super Admin'),
        ),
        migrations.AddField(
            model_name='adminrole',
            name='verified_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='verified_admins',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='adminrole',
            name='verified_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        # Add verified_by field to UserProfile
        migrations.AddField(
            model_name='userprofile',
            name='verified_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='verified_users',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='Profile verified by admin'),
        ),
    ]
