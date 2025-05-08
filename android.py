from flask import Blueprint

bp = Blueprint('android', __name__, url_prefix='/android')

@bp.route('/create', methods=['POST']) #type:ignore
def create():
    pass

