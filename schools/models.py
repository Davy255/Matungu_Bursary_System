from django.db import models
import uuid


class SchoolCategory(models.Model):
    """School category (University, College, TVET)"""
    CATEGORY_CHOICES = (
        ('University', 'University'),
        ('College', 'College'),
        ('TVET', 'Technical and Vocational Education and Training'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'School Categories'
    
    def __str__(self):
        return self.name


class School(models.Model):
    """School model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(SchoolCategory, on_delete=models.CASCADE, related_name='schools')
    county = models.CharField(max_length=100, default='Kakamega')
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True, blank=True, help_text='School code/registration number')
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Campus(models.Model):
    """Campus or branch of a school"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='campuses')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    is_main_campus = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_main_campus', 'name']
        unique_together = ('school', 'name')
        verbose_name_plural = 'Campuses'
    
    def __str__(self):
        return f"{self.school.name} - {self.name}"


class Program(models.Model):
    """Academic program offered by school"""
    PROGRAM_LEVEL_CHOICES = (
        ('Certificate', 'Certificate'),
        ('Diploma', 'Diploma'),
        ('Degree', 'Bachelor Degree'),
        ('Masters', 'Master Degree'),
        ('PhD', 'Doctor of Philosophy'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=50, choices=PROGRAM_LEVEL_CHOICES)
    duration_months = models.IntegerField(default=12)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['school', 'level', 'name']
        unique_together = ('school', 'name')
    
    def __str__(self):
        return f"{self.school.name} - {self.name}"
