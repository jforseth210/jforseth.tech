from flask import *
import os
from werkzeug.utils import secure_filename

file_sharing = Blueprint("file_sharing", __name__)
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py']
UPLOAD_PATH = "uploads"
# This is a magic function from the flask documentation. I have no idea what it does or how it works.


def allowed_file(file_name):
    return '.' in file_name and \
        file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Again. I'd like to change this to file_name, but I think it'd break something.
@file_sharing.route('/filesharing', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        # TODO: Figure out how on earth url_for works
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_PATH, filename))
            return redirect(url_for('file_sharing.uploaded_file', filename=filename))

    else:
        file_list = os.listdir(UPLOAD_PATH)
        return render_template('file_sharing.html', files=file_list)


@file_sharing.route('/filesharing/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_PATH,
                               filename)


@file_sharing.route('/filesharing/filelist')
def file_list():
    files = os.listdir(UPLOAD_PATH)
    return ''.join(files)
