from flask import Blueprint
from flask import render_template

import global_library

connected_bp = Blueprint('connected_bp', __name__, template_folder='templates', static_folder='static')


@connected_bp.route('/')
def connected():
    return render_template('connected.html', title="Connected to Hattrick", from_index=False,
                           ratings=global_library.ratings,
                           positions=global_library.positions, statuses=global_library.statuses)
