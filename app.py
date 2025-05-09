from flask import Flask, request, jsonify
from actions import bp as actions_bp
from filters import bp as filters_bp
from android import bp as android_bp
from helpers import is_allowed_extension, get_secure_filename_filepath

app = Flask(__name__)

app.secret_key = 'MY_API_SECRET'

UPLOAD_FOLDER = 'uploads/'

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jepg']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

app.register_blueprint(actions_bp)
app.register_blueprint(filters_bp)
app.register_blueprint(android_bp)


@app.route('/images', methods=['POST'])
def image_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({ 'error' : 'No file was selected' }), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({ 'error' : 'No file was selected' }), 400
        
        if not is_allowed_extension(file.filename):
            return jsonify({ 'error' : 'The extension is not supported' }), 400
        
        filename, filepath = get_secure_filename_filepath(file.filename)
        
        file.save(filepath)
        return jsonify({
            'message' : 'file successfully uploaded.',
            'filename' : filename, 
        }), 201
    
    return jsonify({ 'message' : 'METHOD NOT ALLOWED' }), 405