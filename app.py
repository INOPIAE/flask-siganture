from flask import Flask, render_template
import os
from flask import  flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime


UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uniqueFilename(filename):
    datetime_object = datetime.now()
    unix_timestamp = datetime_object.timestamp()
    fname=filename.rsplit('.', 1)
    return fname[0] + '_' + str(unix_timestamp) + '.' + fname[1]


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],'signature', uniqueFilename(filename) ))
            return render_template('download_file.html', fname=filename)
    return render_template('upload.html')
