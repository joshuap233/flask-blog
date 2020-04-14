from .blueprint import api
from flask import current_app, send_from_directory


@api.route('/images/image/<filename>')
def send_images_view(filename):
    path = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(path, filename)
