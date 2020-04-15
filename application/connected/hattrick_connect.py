import configparser as c
import os
import tkinter as tk
import tkinter.simpledialog as sd
import webbrowser

from rauth import OAuth1Service
from rauth.oauth import HmacSha1Signature

from application.connected import download_basic_info as d

configuration_file = os.path.abspath('application\connected\session_config.ini')


def read_configuration_file():
    config = c.ConfigParser()
    config.read(configuration_file)
    return config


def configuration_file_has_access_tokens(config):
    if config.has_option('DEFAULT', 'ACCESS_TOKEN') and config.has_option('DEFAULT', 'ACCESS_TOKEN_SECRET'):
        return True
    else:
        return False


def connection_valid():
    # TODO de scris procedura de verificare
    return True


def add_access_tokens_to_config_file(config, connection, request_token, request_token_secret, code):
    access_token, access_token_secret = connection.get_access_token(request_token, request_token_secret,
                                                                    params={'oauth_verifier': code})
    config['DEFAULT']['ACCESS_TOKEN'] = access_token
    config['DEFAULT']['ACCESS_TOKEN_SECRET'] = access_token_secret
    with open(configuration_file, 'w') as configfile:
        config.write(configfile)


def show_pin_window():
    root = tk.Tk()
    root.withdraw()
    code = sd.askstring(title='PIN Required', prompt='Please insert the PIN specified by Hattrick')
    root.destroy()
    return code


def get_access_tokens(config):
    connection = OAuth1Service(consumer_key=config['DEFAULT']['CONSUMER_KEY'],
                               consumer_secret=config['DEFAULT']['CONSUMER_SECRET'], name='Hattrick',
                               request_token_url=config['DEFAULT']['REQUEST_TOKEN_PATH'],
                               access_token_url=config['DEFAULT']['ACCESS_TOKEN_PATH'],
                               authorize_url=config['DEFAULT']['AUTHORIZE_PATH'],
                               base_url=config['DEFAULT']['PROTECTED_RESOURCE_PATH'],
                               signature_obj=HmacSha1Signature)
    request_token, request_token_secret = connection.get_request_token(
        params={'oauth_callback': config['DEFAULT']['CALLBACK_URL']})
    authorization_url = connection.get_authorize_url(request_token)
    webbrowser.open(authorization_url, new=2)
    code = show_pin_window()
    #  TODO: sa tratez cazul in care PIN-ul introdus este gresit
    if code is None:
        return False
    else:
        add_access_tokens_to_config_file(config, connection, request_token, request_token_secret, code)
        return True


def connection_engine():
    # TODO deoarece, in realitate, mai multi utilizatori se vor conecta la aplicatie cu contul de Hattrick,
    #  consumer key, consumer secret, access token si access token secret trebuie puse intr-o baza de date
    #  si luate de acolo, la nevoie. Sau intr-un cookie. Sau altundeva.

    #Functia obtine informatiile de baza despre utilizatorul care s-a conectat.
    #Algoritmul de functionare:
    # 1. Testeaza daca se poate conecta la Hattrick. Asta inseamna ca urmatoarele 2 conditii sa fie adevarate:
    #   1.1. Sa existe jetoanele de acces;
    #   1.2. Conexiunea sa fie permisa de catre Hattrick
    # 2. Daca se poate conecta la Hattrick:
    #   2.1. Descarca informatiile de baza;
    #   2.2. Intoarce True
    # 3. Daca nu se poate conecta la Hattrick:
    #   3.1. Obtine jetoanele de access (efectueaza intreaga procedura de conectare). Daca nu poate, intoarce False
    #   3.2. Descarca informatiile de baza
    #   3.3. Intoarce True.

    config = read_configuration_file()
    if configuration_file_has_access_tokens(config) and connection_valid():
        d.download_basic_info()
        return True
    else:
        if get_access_tokens(config):
            d.download_basic_info()
            return True
        else:
            return False
