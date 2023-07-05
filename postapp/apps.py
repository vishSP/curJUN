from django.apps import AppConfig


class MailingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postapp'
    verbose_name = 'сервис управления рассылками'
