import os, subprocess, time

from flask import Flask, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
STATIC_FILES = 'files/'
UPLOAD_FOLDER = app.root_path + '/' + STATIC_FILES
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp', 'MD', 'md'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/mp', methods=['GET', 'POST'])
def upload_file():
    if 'code' not in request.files:
        return redirect(request.url)

    file = request.files['code']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        created_filename = _create_mp_file(filename)
        print(STATIC_FILES + created_filename)
        return send_from_directory(directory=STATIC_FILES, filename=created_filename)


def _subprocess_cmd(command):
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


def _create_mp_file(filename):
    _subprocess_cmd('cd ' + UPLOAD_FOLDER + ";" + "mptopdf " + filename)
    time.sleep(2)
    return os.path.splitext(filename)[0] + '-0.pdf'
