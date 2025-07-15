from flask import Blueprint, current_app
from flask import Blueprint, request, redirect, url_for, jsonify
from PIL import Image, ImageFilter, ImageEnhance
from helpers import get_secure_filename_filepath, download_from_s3
import os


bp = Blueprint('filters', __name__, url_prefix='/filters')

@bp.route('/blur', methods=['POST']) 
def blur():
    filename = request.json['filename'] #type:ignore
    filename, filepath = get_secure_filename_filepath(filename)
    file_stream = download_from_s3(filename)

    try:
        radius = int(request.json['radius']) #type:ignore
        image = Image.open(file_stream)
        out = image.filter(ImageFilter.GaussianBlur(radius))
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for('download_file', name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found."}), 404




@bp.route('/blur', methods=['POST']) #type:ignore
def contrast():
    filename = request.json['filename'] #type:ignore
    filename, filepath = get_secure_filename_filepath(filename)
    file_stream = download_from_s3(filename)

    try:
        factor = float(request.json['factor']) #type:ignore
        image = Image.open(file_stream)
        out = ImageEnhance.Contrast(image).enhance(factor)
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for('download_file', name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found."}), 404

@bp.route('/brightness', methods=['POST']) #type:ignore
def brightness():
    filename = request.json['filename'] #type:ignore
    filename, filepath = get_secure_filename_filepath(filename)
    file_stream = download_from_s3(filename)

    try:
        factor = float(request.json['factor']) #type:ignore
        image = Image.open(file_stream)
        out = ImageEnhance.Brightness(image).enhance(factor)
        out.save(os.path.join(current_app.config["DOWNLOAD_FOLDER"], filename))
        return redirect(url_for('download_file', name=filename))

    except FileNotFoundError:
        return jsonify({"message": "File not found."}), 404