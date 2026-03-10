import io
import uuid

from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.utils import timezone
from PIL import Image
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application, ApplicationDocument
from schools.models import School
from users.models import UserProfile
from .serializers import (
    ApplicationDocumentSerializer,
    ApplicationSerializer,
    SchoolSerializer,
    UpdateProfileSerializer,
    UserProfileSerializer,
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
        return Response(UserSerializer(request.user, context={'request': request}).data)


class ProfileAPIView(APIView):
    """GET full profile info / PATCH to update name, phone, address etc."""
    permission_classes = [permissions.IsAuthenticated]

    def _get_or_create_profile(self, user):
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'id_number': '',
                'date_of_birth': '2000-01-01',
                'gender': 'O',
                'address': '',
                'county': '',
                'sub_county': '',
                'guardian_name': '',
                'guardian_phone': '',
            }
        )
        return profile

    def get(self, request):
        profile = self._get_or_create_profile(request.user)
        serializer = UserProfileSerializer(profile, context={'request': request})
        data = UserSerializer(request.user, context={'request': request}).data
        data['profile'] = serializer.data
        return Response(data)

    def patch(self, request):
        profile = self._get_or_create_profile(request.user)
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user, context={'request': request}).data)


class UploadProfilePhotoAPIView(APIView):
    """POST a photo (optionally with crop coords) → crops, resizes to 400×400, saves."""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    PROFILE_PHOTO_SIZE = (400, 400)

    def post(self, request):
        photo_file = request.FILES.get('photo')
        if not photo_file:
            return Response({'detail': 'No photo provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate it's an image
        try:
            img = Image.open(photo_file)
            img.verify()          # catch corrupt files early
            photo_file.seek(0)    # reset after verify
            img = Image.open(photo_file)
        except Exception:
            return Response({'detail': 'Invalid image file.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert to RGB to allow saving as JPEG regardless of source format
        img = img.convert('RGB')

        # Optional server-side crop -------------------------------------------
        try:
            crop_x = int(request.data.get('crop_x', 0))
            crop_y = int(request.data.get('crop_y', 0))
            crop_w = int(request.data.get('crop_width', 0))
            crop_h = int(request.data.get('crop_height', 0))
        except (ValueError, TypeError):
            return Response({'detail': 'Crop parameters must be integers.'}, status=status.HTTP_400_BAD_REQUEST)

        if crop_w > 0 and crop_h > 0:
            img_w, img_h = img.size
            # Clamp to image bounds
            crop_x = max(0, min(crop_x, img_w))
            crop_y = max(0, min(crop_y, img_h))
            crop_x2 = min(crop_x + crop_w, img_w)
            crop_y2 = min(crop_y + crop_h, img_h)
            if crop_x2 > crop_x and crop_y2 > crop_y:
                img = img.crop((crop_x, crop_y, crop_x2, crop_y2))

        # Resize to square 400×400 using high-quality Lanczos resampling
        img = img.resize(self.PROFILE_PHOTO_SIZE, Image.Resampling.LANCZOS)

        # Save processed image to in-memory buffer
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=90)
        buffer.seek(0)

        file_name = f"profile_{request.user.pk}_{uuid.uuid4().hex[:8]}.jpg"
        django_file = ContentFile(buffer.read(), name=file_name)

        # Get or create profile and save the photo
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'id_number': '',
                'date_of_birth': '2000-01-01',
                'gender': 'O',
                'address': '',
                'county': '',
                'sub_county': '',
                'guardian_name': '',
                'guardian_phone': '',
            }
        )
        # Delete old photo file to avoid orphaned files
        if profile.profile_photo:
            profile.profile_photo.delete(save=False)
        profile.profile_photo.save(file_name, django_file, save=True)

        photo_url = request.build_absolute_uri(profile.profile_photo.url)
        return Response({
            'detail': 'Profile photo updated successfully.',
            'profile_photo_url': photo_url,
        }, status=status.HTTP_200_OK)


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

