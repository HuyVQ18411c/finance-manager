import os


DATABASE_HOST = os.environ.get('DATABASE_HOST', '')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME', '')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT', ''))
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', '')

DB_URL = 'postgresql://{username}:{password}@{host}:{port}/{name}'.format(
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    name=DATABASE_NAME
)

ALLOW_ORIGINS = [
    'http://127.0.0.1:5500',
    'http://localhost:5500'
    'http://127.0.0.1:8100',
    'http://localhost:8100',
]

ALLOWED_HOST = os.environ.get('ALLOWED_HOST', '0.0.0.0')

USER_CODE_LENGTH = int(os.environ.get('USER_CODE_LENGTH', '6'))
