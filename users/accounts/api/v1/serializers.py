from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer

#from doctors.api.v1.serializers import DoctorProfileRegistrationSerializer, DoctorProfileSerializer
#from doctors.models import DoctorProfile
#from patients.api.v1.serializers import PatientProfileSerializer
#from patients.models import PatientProfile
from subscriptions.api.v1.serializers import SubscriptionSerializer, SubscriptionDetailSerializer

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()

""""
class AccountRegistrationSerializerDoctor(serializers.ModelSerializer):
    profile = DoctorProfileRegistrationSerializer(source='doctor_profile')

    # password = serializers.CharField(max_length=32, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'user_type', 'profile')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            },
            'user': {
                'read_only': True,
            }
        } """

"""def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError(
                _("Password too short. It must contain at least 6 alpha-numeric characters."),
                code='password_too_short',
            )
        if password.isdigit():
            raise serializers.ValidationError(
                _("Password must contain at least 1 digit."),
                code='password_entirely_numeric',
            )
        if password.isalpha():
            raise serializers.ValidationError(
                _("Password must contain at least 1 character."),
                code='password_entirely_characters',
            )

        return password """

def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

"""def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        name = f'{first_name} {last_name}'.strip()
        profile = validated_data.pop('doctor_profile')
        username = generate_unique_username(
            [email, name, 'user']
        )
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            name=name,
            username=username,
            user_type=User.USER_TYPE_DOCTOR
        )
        user.set_password(validated_data.get('password'))
        user.save()
        if user:
            try:
                DoctorProfile.objects.create(user=user, **profile)
            except Exception as err:
                print(err)
        request = self._get_request()
        try:
            setup_user_email(request, user, [])
        except Exception as err:
            print(err)
            print('setup user email error')
        return user """

#def save(self, request=None):
#        """rest_auth passes request so we must override to accept it"""
#return super().save() 

class AccountAuthUserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionDetailSerializer(source='get_subscription', read_only=True, default=None)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'user_type', 'subscription')
        extra_kwargs = {
            'email': {
                'read_only': True
            },
            'user_type': {
                'read_only': True
            }
        }

""" def to_representation(self, instance):
        res = super(self.__class__, self).to_representation(instance)
        if instance.user_type == User.USER_TYPE_DOCTOR:
            try:
                res['profile'] = DoctorProfileSerializer(instance.doctor_profile).data
            except DoctorProfile.DoesNotExist:
                res['profile'] = None
        elif instance.user_type == User.USER_TYPE_PATIENT:
            try:
                res['profile'] = PatientProfileSerializer(instance.patient_profile).data
            except PatientProfile.DoesNotExist:
                res['profile'] = None

    return res"""


"""class AccountAuthUserDoctorSerializer(serializers.ModelSerializer):
    profile = DoctorProfileSerializer(source='doctor_profile', many=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'user_type', 'profile')
        extra_kwargs = {
            'email': {
                'read_only': True
            },
            'user_type': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        res = super(self.__class__, self).to_representation(instance)
        if instance.user_type == User.USER_TYPE_DOCTOR:
            try:
                res['profile'] = DoctorProfileSerializer(instance.doctor_profile).data
            except DoctorProfile.DoesNotExist:
                res['profile'] = None

            from subscriptions.models import Subscription
            try:
                subscription = instance.subscription
            except Subscription.DoesNotExist:
                subscription = None
            # subscription = instance.get_active_subscription()
            if subscription:
                res['subscription'] = SubscriptionSerializer(subscription).data
            else:
                res['subscription'] = None

        elif instance.user_type == User.USER_TYPE_PATIENT:
            try:
                res['profile'] = PatientProfileSerializer(instance.patient_profile).data
            except PatientProfile.DoesNotExist:
                res['profile'] = None

        return res"""

"""def update(self, instance, validated_data):
        if 'doctor_profile' in validated_data:
            profile_serializer = self.fields['profile']
            doctor_profile = validated_data.pop('doctor_profile')
            try:
                profile_instance = instance.doctor_profile
                profile_serializer.update(profile_instance, doctor_profile)
            except DoctorProfile.DoesNotExist:
                DoctorProfile.objects.create(user=instance, **doctor_profile)

        return super(self.__class__, self).update(instance, validated_data)"""


"""class AccountAuthUserPatientSerializer(serializers.ModelSerializer):
    profile = PatientProfileSerializer(source='patient_profile')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'user_type', 'profile')
        extra_kwargs = {
            'email': {
                'read_only': True
            },
            'user_type': {
                'read_only': True
            }
        }"""

"""def to_representation(self, instance):
        res = super(self.__class__, self).to_representation(instance)
        if instance.user_type == User.USER_TYPE_DOCTOR:
            try:
                res['profile'] = DoctorProfileSerializer(instance.doctor_profile).data
            except DoctorProfile.DoesNotExist:
                res['profile'] = None
        elif instance.user_type == User.USER_TYPE_PATIENT:
            try:
                res['profile'] = PatientProfileSerializer(instance.patient_profile).data
            except PatientProfile.DoesNotExist:
                res['profile'] = None

        return res

def update(self, instance, validated_data):
        patient_profile = None
        if 'patient_profile' in validated_data:
            patient_profile = validated_data.pop('patient_profile')
            print(patient_profile)

        res = super(self.__class__, self).update(instance, validated_data)
        if patient_profile:
            try:
                profile = instance.patient_profile
                PatientProfileSerializer().update(profile, patient_profile)

            except PatientProfile.DoesNotExist:
                PatientProfile.objects.create(user=instance, **patient_profile)
        return res """


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""
    password_reset_form_class = ResetPasswordForm
