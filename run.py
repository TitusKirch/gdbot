import os
import logging

import contextlib

from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

from bot import JustGamingBot

load_dotenv()


@contextlib.contextmanager
def setup_logging():

    try:
        # __enter__
        if os.getenv('LOGGING').lower() == 'true':
            if os.getenv('DEBUG').lower() == 'true':
                logging.getLogger('discord').setLevel(logging.DEBUG)
                logging.getLogger('discord.http').setLevel(logging.DEBUG)
            else:
                logging.getLogger('discord').setLevel(logging.INFO)
                logging.getLogger('discord.http').setLevel(logging.WARNING)

            log = logging.getLogger()
            log.setLevel(logging.INFO)
            handler = RotatingFileHandler(
                filename='logs/log.log', encoding='utf-8', mode='w', maxBytes=32 * 1024 * 1024, backupCount=5)
            formatter = logging.Formatter(
                '[{asctime}] [{levelname:<7}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{')
            handler.setFormatter(formatter)
            log.addHandler(handler)

            if os.getenv('DEBUG').lower() == 'true':
                log.info('Logger successfully set up in debug mode')
            else:
                log.info('Logger successfully set up in normal mode')

        yield
    finally:
        # __exit__
        if os.getenv('LOGGING').lower() == 'true':
            handlers = log.handlers[:]
            for handler in handlers:
                handler.close()
                log.removeHandler(handler)


def run_bot():
    # run bot
    bot = JustGamingBot()
    bot.run()


def main():
    with setup_logging():
        run_bot()


if __name__ == '__main__':
    main()
