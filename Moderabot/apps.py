from django.apps import AppConfig
import threading
import asyncio
import os
import django
import sys


class ModerabotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Moderabot'
    bot_thread = None

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        # Configurăm Django dacă nu e configurat
        if not hasattr(django.apps, 'apps'):
            django.setup()

        # Pornim botul doar când rulăm serverul și nu e deja pornit
        if 'runserver' in sys.argv and not self.bot_thread:
            def run_bot():
                import django
                django.setup()
                from Moderabot.disc.bot import run_discord_bot
                asyncio.run(run_discord_bot())

            self.bot_thread = threading.Thread(target=run_bot, daemon=True)
            self.bot_thread.start()