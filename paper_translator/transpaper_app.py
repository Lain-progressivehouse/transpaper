from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import translator

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if pdf_file and allowed_file(pdf_file.filename):
            return translator.get_translate_for_app(pdf_file)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
