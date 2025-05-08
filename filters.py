from flask import Blueprint

bp = Blueprint('filters', __name__, url_prefix='/filters')

@bp.route('/contrast', methods=['POST']) #type:ignore
def contrast():
    pass

@bp.route('/blur', methods=['POST']) #type:ignore
def blur_preset():
    pass

@bp.route('/brightness', methods=['POST']) #type:ignore
def brightness():
    pass