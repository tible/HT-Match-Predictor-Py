class Config:
    """Configurarea serverului"""
    TESTING = True

    """Configurarea bazei de date"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/matches.db'

    """Configurarea parametrilor de conectare la Hattrick"""
    CONSUMER_KEY = 'Cx7jQlJTOwIRA2XVtRWF19'
    CONSUMER_SECRET = 'L1gwHsZZuGneTUwZKUevgBUe3HKIMBDiJv7DHwf1RjI'
    REQUEST_TOKEN_PATH = 'https://chpp.hattrick.org/oauth/request_token.ashx'
    AUTHORIZE_PATH = 'https://chpp.hattrick.org/oauth/authorize.aspx'
    AUTHENTICATE_PATH = 'https://chpp.hattrick.org/oauth/authenticate.aspx'
    ACCESS_TOKEN_PATH = 'https://chpp.hattrick.org/oauth/access_token.ashx'
    CHECK_TOKEN_PATH = 'https://chpp.hattrick.org/oauth/check_token.ashx'
    INVALIDATE_TOKEN_PATH = 'https://chpp.hattrick.org/oauth/invalidate_token.ashx'
    PROTECTED_RESOURCE_PATH = 'https://chpp.hattrick.org/chppxml.ashx'
    CALLBACK_URL = 'oob'

