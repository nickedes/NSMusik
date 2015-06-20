import os
from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request
)
from test_conn import insert
import requests
import json
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    # Fetch all songs in db.
    return "<p>hey</p>"


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        file = request.files['file']
        UPLOAD_FOLDER = '/home/nickedes/'
        ALLOWED_EXTENSIONS = set(['txt'])
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            PATH = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(PATH)
            url = "https://api.idolondemand.com/1/api/sync/analyzesentiment/v1"
            my_api_key = "8adefcc2-a469-4193-ab3f-873bcd71d175"
            f = open(PATH, 'rb')
            r = requests.post(
                url=url, data={'apikey': my_api_key}, files={'file': f})
            data = r.json()
            result = data[data['aggregate']['sentiment']]
            tags = []
            for val in result:
                if val['normalized_text'] not in tags:
                    tags.append(val['normalized_text'])
            print(tags)
            song = {'name':file.filename, 'Path':PATH,'tags':tags}
            ins = insert(song) 
            if ins == True:               
                return 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
