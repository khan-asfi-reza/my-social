  
  
  
  
  
  
  
  
# django imports
from django.contrib.auth import get_user_model
# rest framework imports
from rest_framework.fields import EmailField
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    ValidationError,
    CharField,
)

from rest_framework.validators import UniqueValidator
# django phone number field import
from phonenumber_field.serializerfields import PhoneNumberField
# mysocial app import
from apps.profile.serializers import ProfilePictureSerializer, ProfileSerializer

User = get_user_model()


# User Serializer
class UserSerializer(ModelSerializer):
    """
    Serializer that will be used to create a user and
    preview user's personal details
    """
    query_set = User.objects.all()

    username = CharField(trim_whitespace=True,
                         validators=[
                             UniqueValidator(
                                 queryset=query_set,
                                 message="Username is already used"
                             )
                         ]
                         )
    profile = ProfilePictureSerializer(read_only=True)
    email = EmailField(validators=[
        UniqueValidator(
            queryset=query_set,
            message="Email is already used"
        )
    ],
        default=None,
        required=False,
        allow_null=True,
        allow_blank=True)
    phone_number = PhoneNumberField()
    password = CharField(required=True,
                         style={'input_type': 'password'},
                         trim_whitespace=False,
                         write_only=True)

    class Meta:
        # Model User
        model = User
        # Fields
        fields = ['uuid', 'phone_number', 'profile', 'first_name', 'last_name', 'password', 'username', 'email', ]
        # Read only Fields
        read_only_fields = ['uuid', 'profile']
        # Example
        swagger_example = {
            "phone_number": "+41524204242"
        }

    def create(self, validated_data):
        # Create User
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserPublicBaseSerializer(ModelSerializer):
    """
    Base Serializer
    """
    full_name = CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            "uuid",
            "username",
            "full_name",
            "profile"
        ]
        read_only_fields = [
            "uuid",
            "username",
            "full_name",
            "profile"
        ]


class UserSerializerPublic(UserPublicBaseSerializer):
    """
    User Serializer For Public View
    """
    profile = ProfilePictureSerializer(read_only=True)


class UserSerializerPublicDetails(UserPublicBaseSerializer):
    """
    User Serializer For Public Detail View
    """
    profile = ProfileSerializer(read_only=True)


# Change Password Serializer
class PasswordChangeSerializer(Serializer):
    old_password = CharField(required=True,
                             style={'input_type': 'password'},
                             trim_whitespace=False)
    new_password = CharField(required=True,
                             style={'input_type': 'password'},
                             trim_whitespace=False)

    # Validates OLD password
    def validate(self, attrs):
        request = self.context.get('request')
        old_password = attrs.get('old_password')
        if not request.user.check_password(old_password):
            raise ValidationError({"error": ["Old password is wrong"]})
        return attrs

    # Create new password
    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data.get('new_password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        pass


# Password Forgot Serializer
class ForgotPasswordSerializer(Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    phone_number = CharField(trim_whitespace=True)
    country_code = CharField(trim_whitespace=True)
    password = CharField(trim_whitespace=True, write_only=True, )
