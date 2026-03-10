from django.db import models

class School(models.Model):
    """Educational institutions"""
    SCHOOL_TYPES = [
        ('university', 'University'),
        ('college', 'College'),
        ('tvet', 'TVET Institution'),
        ('polytechnic', 'Polytechnic'),
    ]
    
    name = models.CharField(max_length=200)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    registration_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    county = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Campus(models.Model):
    """School campuses/branches"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='campuses')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school.name} - {self.name}"

    class Meta:
        verbose_name_plural = 'Campuses'
        ordering = ['school', '-is_main', 'name']


class Program(models.Model):
    """Academic programs/courses"""
    PROGRAM_LEVELS = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('degree', 'Degree'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ]
    
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=PROGRAM_LEVELS)
    duration_years = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    class Meta:
        ordering = ['school', 'name']
        unique_together = ['school', 'code']
