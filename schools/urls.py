from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    path('categories/', views.school_categories, name='categories'),
    path('by-category/', views.get_schools_by_category, name='by_category'),
    path('campuses/', views.get_campuses, name='get_campuses'),
    path('programs/', views.get_programs, name='get_programs'),
    path('list/', views.schools_list, name='list'),
    path('<str:school_id>/', views.school_detail, name='detail'),
]
