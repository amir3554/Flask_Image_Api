from flask import Flask, request, jsonify, send_from_directory
from actions import bp as actions_bp
from filters import bp as filters_bp
from android import bp as android_bp
from helpers import is_allowed_extension, get_secure_filename_filepath, upload_to_s3
import boto3, botocore
import secret_info


##############################################################################
# initials
##############################################################################

app = Flask(__name__)

app.secret_key = secret_info.API_SECRET_KEY

app.register_blueprint(actions_bp)
app.register_blueprint(filters_bp)
app.register_blueprint(android_bp)









##############################################################################
# settings 
##############################################################################

DOWNLOAD_FOLDER = 'downloads/'
UPLOAD_FOLDER = 'uploads/'

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jepg']








##############################################################################
# configrations
##############################################################################

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

app.config['S3_BUCKET'] = secret_info.S3_BUCKET
app.config['ACCESS_KEY'] = secret_info.ACCESS_KEY
app.config['ACCESS_SECRET_KEY'] = secret_info.ACCESS_SECRET_KEY
app.config['LOCATION'] = secret_info.LOCATION








##############################################################################
# other oprations
##############################################################################

@app.route('/images', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({ 'error' : 'No file was selected' }), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({ 'error' : 'No file was selected' }), 400
        
        if not is_allowed_extension(file.filename):
            return jsonify({ 'error' : 'The extension is not supported' }), 400
        
        #filename, filepath = get_secure_filename_filepath(file.filename)
        
        #file.save(filepath)
        output = upload_to_s3(file, app.config['S3_BUCKET'])
        if output is None:
            return jsonify({ 'message' : 'S3 upload error ' }), 400
        
        return jsonify({
            'filename' : str(output), 
            'message' : 'file successfully uploaded.',
        }), 201
    
    images = []

    s3_resource = boto3.resource('s3')
    s3_bucket = s3_resource.Bucket(app.config["S3_BUCKET"]) #type:ignore
    for obj in s3_bucket.objects.filter(Prefix='uploads/'):
        if obj.key == 'uploads/':
            continue
        images.append(obj.key)
    return jsonify({ 'data' : images }) , 200



@app.route('/downloads/<name>/')
def download_file(name):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], name)