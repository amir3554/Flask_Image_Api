from flask import Blueprint, request, redirect, jsonify, url_for
from PIL import Image
from helpers import get_secure_filename_filepath

bp = Blueprint('actions', __name__, url_prefix='/actions')

@bp.route('/resize', methods=['POST'])
def resize():
    filename = request.json['filename'] #type:ignore
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        width, height = int(request.json['width']), int(request.json['height'])#type:ignore
        image = Image.open(filepath)
        out = image.resize(width, height)
        out.save(filepath)
        return redirect(url_for('download_file', name=filename))

    except FileNotFoundError:
        return jsonify({ 'message' : 'file not found' }), 404
        

@bp.route('/resize/<preset>', methods=['POST']) #type:ignore
def resize_preset(preset):
    presets = {'small' : (640, 480), 'medium' : (1280, 720), 'large' : (1920, 1080)}
    if preset not in presets:
        return jsonify({'message' : 'preset not avalable.'})

    filename = request.json['filename'] #type:ignore
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        size = presets[preset]
        image = Image.open(filepath)
        out = image.resize(size)
        out.save(filepath)
        return redirect(url_for('download_file', name=filename))

    except FileNotFoundError:
        return jsonify({ 'message' : 'file not found' }), 404

@bp.route('/rotate', methods=['POST']) #type:ignore
def rotate():
    filename = request.json['filename'] #type:ignore
    filename, filepath = get_secure_filename_filepath(filename)

    try:
        digree = float(request.json['degree']) #type:ignore
        image = Image.open(filepath)
        out = image.rotate(digree)
        out.save(filepath)
        return redirect(url_for('download_file', name=filename))

    except FileNotFoundError:
        return jsonify({ 'message' : 'file not found' }), 404
    
@bp.route('/flip', methods=['POST']) #type:ignore
def flip():
    pass