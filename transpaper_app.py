import os

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_cors import CORS

from paper_translator import translator

app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def upload_file():
    print("test")
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if pdf_file and allowed_file(pdf_file.filename):
            document = translator.get_translate(pdf_file, is_file=False)
            response = make_response()
            response.data = document
            download_fileName = os.path.splitext(pdf_file.filename)[0] + ".txt"
            response.headers['Content-Disposition'] = 'attachment; filename=' + download_fileName
            response.mimetype = "text/plain"
            return response
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))

@app.route('/react', methods=['POST'])
def upload_api():
    if request.method == 'POST':
        pdf_file = request.files['file']
        if pdf_file and allowed_file(pdf_file.filename):
            document = translator.get_translate(pdf_file, is_file=False)
            response = make_response()
            response.data = document
            download_fileName = os.path.splitext(pdf_file.filename)[0] + ".txt"
            response.headers['Content-Disposition'] = 'attachment; filename=' + download_fileName
            response.mimetype = "text/plain"
            return response
        else:
            return ''' <p>許可されていない拡張子です</p> '''

if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
