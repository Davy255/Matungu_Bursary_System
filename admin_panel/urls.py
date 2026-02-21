from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('applications/', views.applications_for_review, name='applications_review'),
    path('applications/<str:application_id>/approve/', views.approve_application, name='approve_application'),
    path('applications/<str:application_id>/reject/', views.reject_application, name='reject_application'),
    path('applications/<str:application_id>/details/', views.view_applicant_details, name='applicant_details'),
    path('approved-applicants/', views.approved_applicants_list, name='approved_applicants'),
    path('export-csv/', views.export_approved_csv, name='export_csv'),
    path('manage-admins/', views.manage_admins, name='manage_admins'),
    path('reports/', views.reports_dashboard, name='reports'),
    
    # CDF Admin paths
    path('cdf/approved-applications/', views.cdf_approved_applications, name='cdf_approved_applications'),
    path('cdf/applications/<str:application_id>/award-amount/', views.award_application_amount, name='award_amount'),
    path('cdf/registration-settings/', views.registration_settings, name='registration_settings'),
    path('cdf/rejected-applicants/', views.rejected_applicants, name='rejected_applicants'),
    path('cdf/export-approved-applicants/', views.export_approved_applicants, name='export_approved_applicants'),
]
