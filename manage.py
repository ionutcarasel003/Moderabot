#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import asyncio

def start_bot():
    # Importăm botul aici, după ce Django e inițializat
    from Moderabot.disc.bot import run_discord_bot
    asyncio.run(run_discord_bot())

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moderabot_dj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Pornește botul într-un thread separat doar când rulăm serverul
    if 'runserver' in sys.argv:
        bot_thread = threading.Thread(target=start_bot, daemon=True)
        bot_thread.start()
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()