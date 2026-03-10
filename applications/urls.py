from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/', views.apply, name='apply'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:pk>/', views.view_application, name='view_application'),
    path('<int:pk>/edit/', views.edit_draft, name='edit_draft'),
    path('<int:pk>/upload/', views.upload_documents, name='upload_documents'),
    path('<int:pk>/submit/', views.submit_application, name='submit_application'),
    path('schools/', views.search_schools, name='search_schools'),
]
