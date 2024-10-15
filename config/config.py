class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "12345678-1234-1234-1234-123456789012"
    DATABASE_URI = 'database_uri_here'
    PORT = 4000
    TOKEN_FILE = 'tokennum.txt'
    CONVO_FILE = 'convo.txt'
    MESSAGE_FILE = 'File.txt'
    HATERS_NAME_FILE = 'hatersname.txt'
    TIME_FILE = 'time.txt'

class ProductionConfig:
    DEBUG = False
    SECRET_KEY = "12345678-1234-1234-1234-123456789012"
    DATABASE_URI = 'database_uri_here'
    PORT = 4000
    TOKEN_FILE = 'tokennum.txt'
    CONVO_FILE = 'convo.txt'
    MESSAGE_FILE = 'File.txt'
    HATERS_NAME_FILE = 'hatersname.txt'
    TIME_FILE = 'time.txt'
