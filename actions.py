from flask import Blueprint

bp = Blueprint('actions', __name__, url_prefix='/actions')

@bp.route('/resize', methods=['POST']) #type:ignore
def resize():
    pass

@bp.route('/resize/<preset>', methods=['POST']) #type:ignore
def resize_preset():
    pass

@bp.route('/rotate', methods=['POST']) #type:ignore
def rotate():
    pass
    
@bp.route('/flip', methods=['POST']) #type:ignore
def flip():
    pass