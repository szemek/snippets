from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from os import makedirs
from os.path import join

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!doctype html>
        <title>File Upload</title>
        <h1>Upload a File</h1>
        <form method=post action="/upload" enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if len(file.filename) > 0:
            filename = secure_filename(file.filename)
            file.save(join('uploads', filename))

            return f'File {filename} successfully uploaded'

    return redirect(url_for('index'))

if __name__ == '__main__':
    makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=8000)
