from django.urls import path

from .views import (
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    MyApplicationDetailAPIView,
    MyApplicationListCreateAPIView,
    SchoolListAPIView,
    SubmitApplicationAPIView,
    UploadApplicationDocumentAPIView,
)

app_name = 'api'

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/me/', MeAPIView.as_view(), name='me'),
    path('schools/', SchoolListAPIView.as_view(), name='school_list'),
    path('applications/', MyApplicationListCreateAPIView.as_view(), name='application_list_create'),
    path('applications/<int:pk>/', MyApplicationDetailAPIView.as_view(), name='application_detail'),
    path('applications/<int:pk>/submit/', SubmitApplicationAPIView.as_view(), name='application_submit'),
    path('applications/<int:pk>/documents/', UploadApplicationDocumentAPIView.as_view(), name='application_document_upload'),
]
