from rest_framework import serializers

from applications.models import Application, ApplicationDocument
from schools.models import School
from users.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id_number',
            'date_of_birth',
            'gender',
            'address',
            'county',
            'sub_county',
            'guardian_name',
            'guardian_phone',
            'profile_photo',
            'profile_photo_url',
        ]
        extra_kwargs = {'profile_photo': {'write_only': True}}

    def get_profile_photo_url(self, obj):
        if obj.profile_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
            return obj.profile_photo.url
        return None


class UserSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'is_verified',
            'profile_photo_url',
        ]

    def get_profile_photo_url(self, obj):
        try:
            profile = obj.profile
            if profile.profile_photo:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(profile.profile_photo.url)
                return profile.profile_photo.url
        except UserProfile.DoesNotExist:
            pass
        return None


class UpdateProfileSerializer(serializers.ModelSerializer):
    """For PATCH /api/profile/ - update user + profile fields"""
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    phone_number = serializers.CharField(source='user.phone_number', required=False)

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'date_of_birth',
            'gender',
            'address',
            'county',
            'sub_county',
            'guardian_name',
            'guardian_phone',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'id',
            'name',
            'school_type',
            'registration_number',
            'email',
            'phone_number',
            'address',
            'county',
            'is_active',
        ]


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = [
            'id',
            'document_type',
            'file',
            'file_name',
            'file_size',
            'uploaded_at',
        ]
        read_only_fields = ['file_name', 'file_size', 'uploaded_at']


class ApplicationSerializer(serializers.ModelSerializer):
    documents = ApplicationDocumentSerializer(many=True, read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'application_number',
            'school',
            'school_name',
            'campus',
            'program',
            'admission_number',
            'year_of_study',
            'family_income',
            'amount_requested',
            'amount_approved',
            'reason',
            'status',
            'submitted_at',
            'reviewed_at',
            'approved_at',
            'created_at',
            'updated_at',
            'documents',
        ]
        read_only_fields = [
            'application_number',
            'status',
            'submitted_at',
            'reviewed_at',
            'approved_at',
            'created_at',
            'updated_at',
        ]
