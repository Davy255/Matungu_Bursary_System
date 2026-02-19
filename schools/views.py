from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import School, SchoolCategory, Campus, Program
from .forms import SchoolFilterForm, CampusSelectionForm, ProgramSelectionForm


@require_http_methods(["GET"])
def school_categories(request):
    """API endpoint to get all school categories"""
    categories = SchoolCategory.objects.all().values('id', 'name')
    return JsonResponse({
        'status': 'success',
        'data': list(categories)
    })


@require_http_methods(["GET"])
def get_schools_by_category(request):
    """API endpoint to get schools by category"""
    category_id = request.GET.get('category_id')
    
    if not category_id:
        return JsonResponse({
            'status': 'error',
            'message': 'Category ID is required'
        }, status=400)
    
    schools = School.objects.filter(
        category_id=category_id,
        is_active=True
    ).values('id', 'name', 'location')
    
    return JsonResponse({
        'status': 'success',
        'data': list(schools)
    })


@require_http_methods(["GET"])
def get_campuses(request):
    """API endpoint to get campuses by school"""
    school_id = request.GET.get('school_id')
    
    if not school_id:
        return JsonResponse({
            'status': 'error',
            'message': 'School ID is required'
        }, status=400)
    
    campuses = Campus.objects.filter(
        school_id=school_id,
        is_active=True
    ).values('id', 'name', 'location', 'city')
    
    if not campuses.exists():
        return JsonResponse({
            'status': 'success',
            'data': []
        })
    
    return JsonResponse({
        'status': 'success',
        'data': list(campuses)
    })


@require_http_methods(["GET"])
def get_programs(request):
    """API endpoint to get programs by school"""
    school_id = request.GET.get('school_id')
    
    if not school_id:
        return JsonResponse({
            'status': 'error',
            'message': 'School ID is required'
        }, status=400)
    
    programs = Program.objects.filter(
        school_id=school_id,
        is_active=True
    ).values('id', 'name', 'level', 'duration_months', 'tuition_fee')
    
    return JsonResponse({
        'status': 'success',
        'data': list(programs)
    })


@require_http_methods(["GET"])
def schools_list(request):
    """Display list of schools with filtering"""
    form = SchoolFilterForm(request.GET or None)
    schools = School.objects.filter(is_active=True).select_related('category')
    
    if form.is_valid():
        if form.cleaned_data.get('category'):
            schools = schools.filter(category=form.cleaned_data['category'])
        
        if form.cleaned_data.get('search'):
            search_term = form.cleaned_data['search']
            schools = schools.filter(
                Q(name__icontains=search_term) |
                Q(location__icontains=search_term) |
                Q(description__icontains=search_term)
            )
    
    # Get all categories for filter
    categories = SchoolCategory.objects.all()
    
    context = {
        'schools': schools,
        'categories': categories,
        'form': form,
    }
    return render(request, 'schools/schools_list.html', context)


@require_http_methods(["GET"])
def school_detail(request, school_id):
    """Display detailed view of a single school"""
    school = get_object_or_404(School, id=school_id, is_active=True)
    campuses = school.campuses.filter(is_active=True)
    programs = school.programs.filter(is_active=True)
    
    context = {
        'school': school,
        'campuses': campuses,
        'programs': programs,
    }
    return render(request, 'schools/school_detail.html', context)
