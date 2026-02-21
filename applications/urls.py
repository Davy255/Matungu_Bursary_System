from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Applicant URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('track/', views.track_application, name='track'),
    path('new/step1/', views.new_application_step1, name='new_step1'),
    path('new/<str:application_id>/step2/', views.new_application_step2, name='new_step2'),
    path('new/<str:application_id>/step3/', views.new_application_step3, name='new_step3'),
    path('new/<str:application_id>/step4/', views.new_application_step4, name='new_step4'),
    path('<str:application_id>/', views.application_detail, name='detail'),
    path('<str:application_id>/download/', views.download_application_pdf, name='download'),
    path('<str:application_id>/upload-document/', views.upload_document, name='upload_document'),
    path('document/<str:doc_id>/delete/', views.delete_document, name='delete_document'),
    path('<str:application_id>/update-ward/', views.update_ward, name='update_ward'),
    path('<str:application_id>/delete/', views.delete_application, name='delete_application'),
    path('<str:application_id>/add-comment/', views.add_application_comment, name='add_comment'),
    
    # Admin URLs
    path('admin/list/', views.admin_applications_list, name='admin_list'),
    path('admin/<str:application_id>/review/', views.admin_review_application, name='admin_review'),
    path('admin/export-approved/', views.export_approved_applications, name='export_approved'),
]
