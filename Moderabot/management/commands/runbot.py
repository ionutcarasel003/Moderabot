from django.core.management.base import BaseCommand
import os
import django
import asyncio
from Moderabot.disc.bot import run_discord_bot

class Command(BaseCommand):
    help = 'Runs the Discord bot with Django integration'

    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moderabot_dj.settings')
        django.setup()
        
        # Rulează botul Discord
        asyncio.run(run_discord_bot()) 