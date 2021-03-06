# Biblioteca citeste fisierele XML si intoarce datele necesare, sub forma de dictionar
import xml.etree.ElementTree as ET

import global_library


def parse_user_file():
    data = {}
    tree = ET.parse(global_library.user_savepath)
    root = tree.getroot()
    data['user name'] = root[4][1].text
    data['user id'] = root[4][0].text
    data['supporter'] = root[4][2].text
    data['country'] = root[4][4][1].text
    data['country id'] = root[4][4][0].text
    data['team 1 name'] = root[4][5][0][1].text
    data['team 1 id'] = root[4][5][0][0].text
    number_of_user_teams = len(list(root[4][5]))
    if number_of_user_teams == 1:
        data['team 2 name'] = 'None'
        data['team 2 id'] = '-'
        data['team 3 name'] = 'None'
        data['team 3 id'] = '-'
    elif number_of_user_teams == 2:
        data['team 2 name'] = root[4][5][1][1].text
        data['team 2 id'] = root[4][5][1][0].text
        data['team 3 name'] = 'None'
        data['team 3 id'] = '-'
    else:
        data['team 2 name'] = root[4][5][1][1].text
        data['team 2 id'] = root[4][5][1][0].text
        data['team 3 name'] = root[4][5][2][1].text
        data['team 3 id'] = root[4][5][2][0].text
    return data


def parse_matches_file():
    data = []
    tree = ET.parse(global_library.matches_savepath)
    root = tree.getroot()
    match_list = root[5][5]
    for match in match_list:
        for i in range(len(match)):
            if match[i].tag == 'MatchType' and match[i].text in ['1', '4', '8', '10', '12']:
                for j in range(i, len(match)):
                    if match[j].tag == 'Status' and match[j].text == 'UPCOMING':
                        match_id = match[0].text
                        home_team = match[1][1].text
                        away_team = match[2][1].text
                        data.append((match_id, home_team, away_team))
    return data


def parse_match_details_file(match_id):
    match_details = [match_id]
    tree = ET.parse(global_library.details_savepath)
    root = tree.getroot()
    for i in range(7, 14, 1):
        match_details = match_details + [root[6][9][i].text]  # evaluarile echipei de acasa
    for i in range(7, 14, 1):
        match_details = match_details + [root[6][10][i].text]  # evaluarile echipei din deplasare
    match_details = match_details + [root[6][9][4].text]  # numarul de goluri ale echipei de acasa
    match_details = match_details + [root[6][10][4].text]  # numarul de goluri ale echipei din deplasare
    return match_details


def parse_future_match_file():
    ratings = ()
    tree = ET.parse(global_library.orders_savepath)
    root = tree.getroot()
    match_data = root[6]
    for i in range(2, 9, 1):
        ratings = ratings + (match_data[i].text,)
    return ratings


def parse_connection_verification_file():
    tree = ET.parse(global_library.check_connection_savepath)
    root = tree.getroot()
    try:
        root[4].text
    except IndexError:  # asta inseamna ca fisierul cu extensia xml este, de fapt, un fisier HTML si acel nod nu exista.
        # Ar da mesajul de eroare: IndexError: child index out of range
        return False
    else:
        return True
