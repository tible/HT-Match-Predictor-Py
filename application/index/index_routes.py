# Defineste rutele pentru pagina de index

import datetime
import os.path
import xml.etree.ElementTree as ET
import zipfile as z

from flask import Blueprint
from flask import render_template
from flask import request

import application.dialog_windows as dw
import global_library
from application.admin import create_db
from application.admin import delete_db
from application.admin import import_matches
from application.connected import download_future_match
from application.connected import download_user_matches
from application.connected import hattrick_connect
from application.connected import hattrick_disconnect
from application.estimation import estimation_engine

index_bp = Blueprint('index_bp', __name__, template_folder='templates', static_folder='static')


# Functia intoarce numele echipei selectate pentru a-i afla viitoarele meciuri
def get_user_team_name():
    if global_library.team_id == global_library.user_data['team 1 id']:
        return global_library.user_data['team 1 name']
    elif global_library.team_id == global_library.user_data['team 2 id']:
        return global_library.user_data['team 2 name']
    else:
        return global_library.user_data['team 3 name']


# Functia arata daca echipa test_team joaca acasa sau in deplasare
def home_or_away(match_id, test_team):
    real_home_team = ''
    match_list = ET.parse(global_library.matches_savepath).getroot()[5][5]
    for match in match_list.findall('Match'):
        if match_id == match[0].text:
            real_home_team = match[1][1].text
            break
    return 'Home' if test_team == real_home_team else 'Away'


# index
@index_bp.route('/')
def home():
    return render_template('index.html', title="The Best Match Predictor", ratings=global_library.ratings,
                           positions=global_library.positions,
                           statuses=global_library.statuses, from_index=True,
                           match_orders=global_library.default_match_orders,
                           answer=global_library.ans)


# conectarea la Hattrick
@index_bp.route('/LoginToHattrick')
def LoginToHattrick():
    connection_successful, global_library.user_data = hattrick_connect.connection_engine()
    if connection_successful:
        return render_template('connected.html', title="Connected to Hattrick", from_index=False,
                               ratings=global_library.ratings,
                               positions=global_library.positions, statuses=global_library.statuses,
                               user_data=global_library.user_data,
                               match_orders=global_library.default_match_orders,
                               answer=global_library.ans)
    else:
        return render_template('index.html', title="The Best Match Predictor", ratings=global_library.ratings,
                               positions=global_library.positions,
                               statuses=global_library.statuses, from_index=True, answer=global_library.ans,
                               match_orders=global_library.default_match_orders)


# algoritmul de estimare
@index_bp.route('/EstimationEngine', methods=['POST'])
def estimation():
    return render_template('index.html', title="The Best Match Predictor", ratings=global_library.ratings,
                           positions=global_library.positions,
                           statuses=global_library.statuses, from_index=True,
                           match_orders=global_library.default_match_orders,
                           answer=estimation_engine.estimate_results(given_ratings=[i for i in request.form.values()]))


# deconectarea de la Hattrick
@index_bp.route('/DisconnectFromHattrick')
def disconnect_from_hattrick():
    hattrick_disconnect.disconnection_engine()
    return render_template('index.html', title="The Best Match Predictor",
                           ratings=global_library.ratings, positions=global_library.positions,
                           statuses=global_library.statuses, from_index=True,
                           match_orders=global_library.default_match_orders,
                           answer=global_library.ans)


# importarea de meciuri in baza de date
@index_bp.route('/import', methods=['POST'])
def import_matches_into_database():
    import_matches.import_engine(low_end=int(request.form['InferiorLimit']),
                                 high_end=int(request.form['SuperiorLimit']))
    dw.show_info_window_in_thread(title='Import terminat', message='Am importat toate meciurile alese')
    return render_template('admin.html', title='Admin Control Panel')


# iesirea din panoul de control catre prima pagina
@index_bp.route('/LogoutToIndex')
def logout():
    match_orders = global_library.default_match_orders
    return render_template('index.html', title="The Best Match Predictor",
                           ratings=global_library.ratings, positions=global_library.positions,
                           statuses=global_library.statuses, from_index=True, match_orders=match_orders,
                           answer=global_library.ans)


# crearea bazei de date
@index_bp.route('/create')
def create():
    create_db.create_database()
    return render_template('admin.html')


# stergerea bazei de date
@index_bp.route('/delete')
def delete():
    delete_db.delete_database()
    return render_template('admin.html')


# Intoarce numele echipei selectate
@index_bp.route('/Team', methods=['POST'])
def get_team_id():
    team_id = request.form['HattrickTeams']
    global_library.team_id = team_id
    global_library.user_team_name = get_user_team_name()
    user_matches = download_user_matches.download_user_matches(team_id)
    global_library.user_matches = user_matches
    match_orders = global_library.default_match_orders
    return render_template('connected.html', title="Connected to Hattrick", from_index=False,
                           ratings=global_library.ratings,
                           positions=global_library.positions, statuses=global_library.statuses,
                           user_data=global_library.user_data,
                           user_matches=user_matches, match_orders=match_orders, answer=global_library.ans)


# Intoarce numarul de identificare al unui meci selectat
@index_bp.route('/GetMatch', methods=['POST'])
def get_match_id():
    match_id = request.form['FutureMatches']
    match_orders = download_future_match.download_future_match(match_id, global_library.team_id)
    place = home_or_away(match_id, global_library.user_team_name)
    return render_template('connected.html', title="Connected to Hattrick", from_index=False,
                           ratings=global_library.ratings,
                           positions=global_library.positions, statuses=global_library.statuses,
                           user_data=global_library.user_data,
                           user_matches=global_library.user_matches, match_orders=match_orders, place=place,
                           answer=global_library.ans)


@index_bp.route('/backup')
def backup_database():
    archive_name = global_library.database_backup_path + '\\backup ' + datetime.datetime.now().strftime(
        '%Y-%m-%d %H-%M-%S') + '.zip'
    with z.ZipFile(file=archive_name, mode='w') as backup:
        backup.write(global_library.database_file_path,
                     arcname='matches.db')
    dw.show_info_window_in_thread(title='Backup terminat', message='Am terminat backupul bazei de date.')
    return render_template('admin.html')


@index_bp.route('/restore')
def restore_database():
    restore_database_file_name = dw.restore_backup_window_in_thread()
    with z.ZipFile(restore_database_file_name, 'r') as restore:
        restore.extractall(os.path.dirname(global_library.database_file_path))
    dw.show_info_window_in_thread(title='Restaurare incheiata', message='S-a incheiat restaurarea backupului ales')
    return render_template('admin.html')
