import os
from flask import current_app
from werkzeug.utils import secure_filename


def is_allowed_extension(filename) -> bool:

    file_parts_list : list = filename.rsplit('.', 1)

    allowed_extensions : list = current_app.config['ALLOWED_EXTENSIONS']

    return ('.' in filename) and (file_parts_list[1].lower() in allowed_extensions)

def get_secure_filename_filepath(filename) -> tuple:
    filename_secure = secure_filename(filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    return filename_secure, filepath
