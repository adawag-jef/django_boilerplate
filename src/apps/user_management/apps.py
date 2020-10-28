from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    name = 'user_management'

    def ready(self):
        from notifier import signals
