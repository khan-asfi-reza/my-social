from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Account app config
    This app handles account information flow
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.accounts'
