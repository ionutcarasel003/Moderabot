from django.apps import AppConfig
# from disc.bot import run_discord_bot


class ModerabotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Moderabot'

    def ready(self):

        pass