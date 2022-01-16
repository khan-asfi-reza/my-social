from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User


# Register your models here.


# The Customized User Admin Interface
class UserAdminInterface(BaseUserAdmin):
    # Change Password Form
    change_password_form = PasswordChangeForm
    # Add User Form
    form = UserAdminChangeForm
    # Add User Form
    add_form = UserAdminCreationForm
    # List of information that will be displayed in the table of User Model Admin Panel
    list_display = ('username', 'id', 'phone_number')
    # Filter Users using verified and gender
    list_filter = ('is_superuser', 'is_active')
    # Fields Sets For Each User's information
    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'country_code',)}),
        ('Personal info', {'fields': ('gender', 'email')}),
    )
    # Add User Form Fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2',)}
         ),
    )
    # Profile Admin Panel and Profile Package Admin Panel
    # Search using phone number and username
    search_fields = ('phone_number', 'username')
    # Order Using Id
    ordering = ('-id',)
    filter_horizontal = ()


# Registering in admin panel
admin.site.register(User, UserAdminInterface)
