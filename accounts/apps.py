from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    def ready(self):
        """Import signal handlers when app is ready."""
        import accounts.signals

