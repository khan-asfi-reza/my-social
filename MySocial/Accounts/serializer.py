from django.contrib.auth import get_user_model, authenticate
from rest_framework.fields import EmailField
from rest_framework.serializers import Serializer, ModelSerializer, ValidationError, CharField, SerializerMethodField, \
    IntegerField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from MySocial.settings import STRIPE_SECRET_KEY
from .models import RefCode, OTP
import stripe

stripe.api_key = STRIPE_SECRET_KEY
User = get_user_model()


# User Serializer
class UserSerializer(ModelSerializer):
    query_set = User.objects.all()

    # Customized Fields

    # Username Field with Unique Validator
    name = CharField(trim_whitespace=True,
                     validators=[UniqueValidator(queryset=query_set, message="Username is already used")])
    # Email Field with Unique Validator with Blank True
    email = EmailField(validators=[UniqueValidator(queryset=query_set, message="Email is already used")],
                       write_only=True, default=None, required=False, allow_null=True, allow_blank=True)
    # Phone Number Country Code
    country_code = CharField(write_only=True,
                             required=False,
                             default="+1",
                             allow_null=True,
                             allow_blank=True)
    # Phone Number
    phone_number = CharField(write_only=True)
    # Password
    password = CharField(required=True,
                         style={'input_type': 'password'},
                         trim_whitespace=False,
                         write_only=True)

    class Meta:
        # Model User
        model = User
        # Fields
        fields = ['id', 'phone_number', 'password', 'gender', 'username', 'email', 'country_code']
        # Read only Fields
        read_only_fields = ['id', ]

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=["phone_number", "country_code"],
                message="Phone Number is already used",
            ),

        ]

    # Validates User Info and creates
    def validate(self, attrs):
        if self.context.get('request').method == 'POST':
            try:
                # Check if phone number is verified, create account, or send error
                otp_object = OTP.objects.get(phone_number=attrs.get('phone_number'),
                                             country_code=attrs.get('country_code'),
                                             use_case=1
                                             )
                # If Otp is verified return validated data, Or Raise Error
                if otp_object.verified:
                    otp_object.delete()
                    return attrs
                else:
                    raise ValidationError({'error': ['Phone number not verified']})
            except OTP.DoesNotExist:
                raise ValidationError({'error': ['Phone number not verified, Unable to verify']})
        else:
            return attrs

    def create(self, validated_data):
        # Create stripe customer account
        obj = stripe.Customer.create(
            description="user created",
            name=validated_data['username'],
            email=validated_data['email']
        )
        # Create User
        user = User(stripe_id=dict(obj)['id'], **validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# Authenticate User Using username and password, returns validated user data after authentication
class AuthenticationSerializer(Serializer):

    # Username
    name = CharField(required=True, trim_whitespace=True)
    # Password
    password = CharField(required=True,
                         style={'input_type': 'password'},
                         trim_whitespace=False)

    # Validate username and password, returns Auth User
    def validate(self, attrs):
        # Validate and authenticate
        name = attrs.get('username')
        password = attrs.get('password')
        if not User.objects.filter(name=name).exists():
            raise ValidationError({'error': 'Account does not exist'}, code='authentication')
        user = authenticate(request=self.context.get('request'),
                            name=name,
                            password=password)
        if not user:
            msg = "Username or password is wrong"
            raise ValidationError({'error': msg}, code='authentication')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


# Ref Code Validation Serializer to validate ref code
class RefCodeValidation(ModelSerializer):
    # Validity check of ref code
    class Meta:
        model = RefCode
        fields = ['id', 'ref_code', 'owner', 'referred']
        read_only_fields = ['id', 'owner']


# Ref Code Create Serializer to View and create
class RefCodeCreate(ModelSerializer):
    referred = SerializerMethodField()

    @staticmethod
    def get_referred(obj):
        return obj.referred.username if obj.referred is not None else ""

    class Meta:
        model = RefCode
        fields = ['id', 'ref_code', 'owner', 'referred']
        read_only_fields = ['id', 'owner', 'ref_code', 'referred']


# OTP Model serializer,
class OTPSerializer(ModelSerializer):
    # Fields
    otp = IntegerField()
    phone_number = CharField(trim_whitespace=True)
    country_code = CharField(trim_whitespace=True)
    use_case = IntegerField(required=False, allow_null=True, write_only=True)

    # Meta Class
    class Meta:
        model = OTP
        fields = ['id', 'phone_number', 'otp', 'country_code', 'use_case', 'verified']
        read_only_fields = ['id', 'verified']

    # Validates if OTP Instance with this phone number exxists
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        country_code = attrs.get('country_code')

        if OTP.objects.filter(phone_number=phone_number, country_code=country_code).exists():
            return attrs
        raise ValidationError({'error': ["OTP Doesn't exist"]})

    # Checks OTP and Save
    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        country_code = validated_data['country_code']
        use_case = validated_data.get('use_case', 1)
        otp_object = OTP.objects.get(phone_number=phone_number, country_code=country_code)
        if validated_data['otp'] == otp_object.otp:
            otp_object.verified = True
            otp_object.use_case = use_case
            otp_object.save()
            return otp_object
        else:
            raise ValidationError({'error': ["OTP Doesn't match"]})


# Class OTP Phone Number Serializer -> Returns validated data
class OTPValidateSerializer(Serializer):
    phone_number = CharField(trim_whitespace=True)
    country_code = CharField(trim_whitespace=True)
    use_case = IntegerField(required=False, allow_null=True, write_only=True)

    # Validates phone number
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        country_code = attrs.get('country_code')
        # If use case is forgot password, check if phone number exists
        if attrs.get('use_case', None) == 2:
            try:
                User.objects.get(phone_number=phone_number, country_code=country_code)
            except User.DoesNotExist:
                return ValidationError({'error': ["Phone number doesn't exist"]})
        # Delete Pre Existing OTP
        otp_object = OTP.objects.filter(phone_number=phone_number, country_code=country_code)
        if otp_object.exists():
            otp_object.delete()
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


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
    phone_number = CharField(trim_whitespace=True)
    country_code = CharField(trim_whitespace=True)
    password = CharField(trim_whitespace=True, write_only=True, )

    # Validates Data
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        country_code = attrs.get('country_code')
        try:
            otp = OTP.objects.get(phone_number=phone_number, country_code=country_code, use_case=2)
            if otp.verified:
                otp.delete()
                return attrs
            else:
                raise ValidationError({'error': ["Phone number not verified"]})
        except OTP.DoesNotExist:
            raise ValidationError({'error': ["OTP Doesn't exist"]})

    # Creates Data
    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        country_code = validated_data['country_code']
        password = validated_data['password']
        user = User.objects.get(phone_number=phone_number, country_code=country_code)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        pass
