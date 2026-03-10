import uuid

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application, ApplicationDocument
from schools.models import School
from .serializers import (
    ApplicationDocumentSerializer,
    ApplicationSerializer,
    SchoolSerializer,
    UserSerializer,
)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'detail': 'Logged out successfully.'})


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class SchoolListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolSerializer

    def get_queryset(self):
        queryset = School.objects.filter(is_active=True)
        query = self.request.query_params.get('q', '').strip()
        school_type = self.request.query_params.get('type', '').strip()

        if query:
            queryset = queryset.filter(name__icontains=query)
        if school_type:
            queryset = queryset.filter(school_type=school_type)

        return queryset.order_by('name')


class MyApplicationListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related('school', 'campus', 'program')

    def perform_create(self, serializer):
        serializer.save(
            applicant=self.request.user,
            application_number=f"BUR-{timezone.now().year}-{uuid.uuid4().hex[:8].upper()}",
            status='draft',
        )


class MyApplicationDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related('school', 'campus', 'program')


class SubmitApplicationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk, applicant=request.user)

        if application.status != 'draft':
            return Response({'detail': 'This application has already been submitted.'}, status=status.HTTP_400_BAD_REQUEST)

        required_docs = {'id', 'admission', 'fee_structure'}
        uploaded_types = set(application.documents.values_list('document_type', flat=True))
        missing = sorted(required_docs - uploaded_types)

        if missing:
            return Response(
                {'detail': 'Missing required documents.', 'missing_documents': missing},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = 'submitted'
        application.submitted_at = timezone.now()
        application.save(update_fields=['status', 'submitted_at', 'updated_at'])

        return Response(ApplicationSerializer(application).data, status=status.HTTP_200_OK)


class UploadApplicationDocumentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationDocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        application = get_object_or_404(Application, pk=kwargs['pk'], applicant=request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data['file']
        document = ApplicationDocument.objects.create(
            application=application,
            document_type=serializer.validated_data['document_type'],
            file=uploaded_file,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
        )

        return Response(ApplicationDocumentSerializer(document).data, status=status.HTTP_201_CREATED)
