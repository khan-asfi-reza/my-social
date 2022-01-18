from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import User


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    # Name is username
    username = forms.CharField(label='UserName')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    # Phone number input
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
                                   label="Phone number", required=True)
    # Email Input - Not Required
    email = forms.EmailField(label='Email Address', required=False)
    # Password and confirm password
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', )

    # Clean Email, checks if email is used or not
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # If email is not none or empty, check if email is used
        if email is not None or email != "":
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("Email is already taken")
            return email

    # Clean Phone Number, checks if phone number is used or not
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        country_code = self.cleaned_data.get('country_code')
        qs = User.objects.filter(phone_number=phone_number, country_code=country_code)
        if qs.exists():
            raise forms.ValidationError("Phone Number is already taken")
        return phone_number

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('phone_number', 'username', 'email',)

    def clean_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class AdminCreationForm(UserAdminCreationForm):
    """
        A form for creating new admin/staff. Includes all the required
        fields, plus a repeated password.
    """

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'username', )

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
