# Development Guide

This guide is for developers who want to contribute to or extend the Bursary Management System.

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/bursary-system.git
cd bursary-system
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies with dev tools
pip install -r requirements.txt
pip install django-debug-toolbar  # For debugging
pip install black  # Code formatter
pip install flake8  # Linter
pip install pytest  # Testing framework
```

### 3. Configure Development Settings

Create `.env.dev`:
```
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=bursary_system_dev
DB_USER=root
DB_PASSWORD=password
```

### 4. Initialize Development Database

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_schools
```

## Project Structure

```
Bursary_system/
├── bursary_system/        # Project configuration
├── users/                 # User management
├── schools/              # School directory
├── applications/         # Main application logic
├── notifications/        # Email/SMS
├── admin_panel/         # Admin dashboard
├── templates/           # HTML files
├── static/              # CSS/JS/Images
└── media/               # User uploads
```

## Code Style & Standards

### Python Style Guide (PEP 8)

```bash
# Format code
black .

# Check style
flake8 .
```

### Django Best Practices

1. **Models**: Keep business logic in models
2. **Views**: Keep views thin, use services
3. **Forms**: Use forms for validation
4. **Templates**: Limit logic, use template tags
5. **URLs**: Keep URL patterns organized

### Example Model

```python
from django.db import models
import uuid

class MyModel(models.Model):
    """Description of the model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'My Models'
    
    def __str__(self):
        return self.name
```

### Example View

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def my_view(request):
    """View description"""
    if request.method == 'POST':
        # Handle POST
        return redirect('app:url_name')
    
    context = {'key': 'value'}
    return render(request, 'template.html', context)
```

## Creating New Features

### 1. Create New Model

```bash
cd app_name
# Edit models.py
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Forms

```python
# forms.py
from django import forms
from .models import MyModel

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['name', 'description']
```

### 3. Create Views

```python
# views.py
from django.shortcuts import render
from .models import MyModel
from .forms import MyModelForm

def list_view(request):
    objects = MyModel.objects.all()
    return render(request, 'list.html', {'objects': objects})
```

### 4. Add URLs

```python
# urls.py (app-level)
from django.urls import path
from . import views

app_name = 'app_name'

urlpatterns = [
    path('', views.list_view, name='list'),
]

# urls.py (project-level)
urlpatterns = [
    path('app/', include('app_name.urls')),
]
```

### 5. Create Templates

```html
<!-- templates/app_name/list.html -->
{% extends 'base.html' %}

{% block content %}
    <h1>List</h1>
    {% for object in objects %}
        <p>{{ object.name }}</p>
    {% endfor %}
{% endblock %}
```

### 6. Register in Admin

```python
# admin.py
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
```

## Testing

### Run Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test users

# Specific test class
python manage.py test users.tests.UserTestCase

# Specific test method
python manage.py test users.tests.UserTestCase.test_create_user
```

### Write Tests

```python
# tests.py
from django.test import TestCase
from django.contrib.auth.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
```

## Database Management

### Create Migration

```bash
python manage.py makemigrations
python manage.py makemigrations app_name
```

### Show SQL

```bash
python manage.py sqlmigrate app_name 0001
```

### Revert Migration

```bash
python manage.py migrate app_name 0001
```

### Create Empty Migration

```bash
python manage.py makemigrations --empty app_name --name migration_name
```

## Debugging

### Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    'debug_toolbar',
    ...
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ...
]

INTERNAL_IPS = ['127.0.0.1']
```

### Django Shell

```bash
python manage.py shell

# Example
from users.models import UserProfile
users = UserProfile.objects.all()
print(users.count())
```

### Print SQL Queries

```python
from django.db import connections
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connections['default']) as context:
    # Your code here
    pass

print(context.captured_queries)
```

## Git Workflow

### Create Branch

```bash
git checkout -b feature/my-feature
```

### Make Changes

```bash
git add .
git commit -m "feat: add my feature"
```

### Push to Remote

```bash
git push origin feature/my-feature
```

### Create Pull Request

- Go to GitHub
- Click "New Pull Request"
- Select your branch
- Add description
- Request review

## Commit Message Convention

```
feat: add new feature
fix: fix a bug
docs: update documentation
style: code style changes
refactor: refactor code
perf: performance improvements
test: add tests
chore: update dependencies
```

## Common Tasks

### Add New Admin Role

```python
# In admin panel or shell
from users.models import AdminRole
from django.contrib.auth.models import User

user = User.objects.get(username='admin')
AdminRole.objects.create(
    user=user,
    role_type='Ward_Admin',
    ward='Matungu',
    assigned_by=User.objects.filter(is_superuser=True).first()
)
```

### Add New School

```bash
python manage.py shell

from schools.models import School, SchoolCategory

category = SchoolCategory.objects.get(name='University')
School.objects.create(
    name='New University',
    category=category,
    location='Nairobi',
    code='NU001'
)
```

### Create Email Template

```bash
# Via admin or shell
from notifications.models import EmailTemplateContentType

EmailTemplateContentType.objects.create(
    template_type='application_submitted',
    subject='Application Submitted',
    body='Your application has been submitted successfully',
    is_active=True
)
```

## Performance Tips

1. **Use select_related()** for ForeignKey
   ```python
   applications = Application.objects.select_related('applicant', 'school')
   ```

2. **Use prefetch_related()** for ManyToMany
   ```python
   users = User.objects.prefetch_related('groups')
   ```

3. **Add database indexes**
   ```python
   class MyModel(models.Model):
       name = models.CharField(max_length=100, db_index=True)
   ```

4. **Use pagination**
   ```python
   from django.core.paginator import Paginator
   paginator = Paginator(queryset, 20)
   page = paginator.get_page(1)
   ```

5. **Cache queries**
   ```python
   from django.core.cache import cache
   data = cache.get_or_set('key', queryset, 3600)
   ```

## Security Best Practices

1. **Input Validation**: Always validate user input
2. **SQL Injection**: Use ORM, never raw SQL
3. **XSS Protection**: Use template escaping
4. **CSRF Protection**: Include {% csrf_token %}
5. **Authentication**: Use Django's built-in auth
6. **Permissions**: Always check permissions
7. **Secrets**: Never commit secrets, use .env

## Useful Resources

- **Django ORM**: Querysets, aggregation, annotations
- **Django Signals**: Pre/post save hooks
- **Django Middleware**: Request/response processing
- **Context Processors**: Template context injection
- **Template Tags**: Custom template functions
- **Decorators**: Function/class decorators

## Documentation

When creating new features:

1. **Document** the function/class
   ```python
   def my_function():
       """
       Short description.
       
       Longer description if needed.
       
       Args:
           arg1: Description
       
       Returns:
           Description
       """
   ```

2. **Update README**
3. **Add docstrings**
4. **Comment complex logic**
5. **Update this guide**

## Troubleshooting

### Migrations Won't Migrate

```bash
python manage.py showmigrations
python manage.py makemigrations --dry-run
```

### Import Errors

```bash
# Reinstall in development mode
pip install -e .
```

### Circular Imports

- Move imports inside functions
- Use TYPE_CHECKING for type hints
- Restructure code

## Release Checklist

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Version bumped
- [ ] CHANGELOG updated
- [ ] Tag created
- [ ] Release notes written

---

**Happy Coding!** 🚀

For questions or issues, please open a GitHub issue or contact the team.
