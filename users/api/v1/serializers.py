from rest_framework import serializers

from doctors.api.v1.serializers import DoctorProfileSerializer
from patients.api.v1.serializers import PatientProfileSerializer
from users.models import User


class DoctorUserBasicInfoSerializer(serializers.ModelSerializer):
    profile = DoctorProfileSerializer(source='doctor_profile', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')


class PatientUserBasicInfoSerializer(serializers.ModelSerializer):
    profile = PatientProfileSerializer(source='patient_profile', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')
