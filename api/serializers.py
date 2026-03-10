from rest_framework import serializers

from applications.models import Application, ApplicationDocument
from schools.models import School
from users.models import User


class UserSerializer(serializers.ModelSerializer):
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
        ]


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
