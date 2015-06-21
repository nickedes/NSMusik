import operator
import os
from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request
)
import re
from test_conn import (
    insert,
    view
)
import requests
import json
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

keywords = ['stormy', 'drunk', 'lonely', 'tired', 'sorry', 'lost',
            'respect', 'love', 'depressed', 'jealous', 'mesmerize']


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    # Fetch all songs in db.
    data = view()
    if data != "hey":
        for value in data:
            data[value]['tags'] = json.loads(data[value]['tags'])
    return render_template('songs.html', data=data)


def getWords(text):
    return re.compile('\w+').findall(text)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        file = request.files['file2']
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
            tags = {}
            for val in result:
                if val['normalized_text'] not in tags:
                    list_tags = getWords(val['normalized_text'])
                    for x in list_tags:
                        if x not in tags:
                            if x in keywords:
                                tags[x] = 1
                        else:
                            tags[x] += 1
            print(tags)
            sorted_tags = sorted(tags.items(), key=operator.itemgetter(0))
            if len(sorted_tags) > 5:
                sorted_tags = sorted_tags[0:5]

            if sorted_tags.reverse():
                sorted_tags = sorted_tags.reverse()
            tags = json.dumps(sorted_tags)
            file = request.files['file1']
            ALLOWED_EXTENSIONS = set(['mp3'])
            if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
                filename = secure_filename(file.filename)
                PATH = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(PATH)
                song = {'name': file.filename, 'Path': PATH, 'tags': tags}
                ins = insert(song)
                if ins == True:
                    return redirect(url_for('home'))
                else:
                    print ins
                    return render_template('data.html', msg=ins)
            else:
                return render_template('data.html', msg="error")

if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=PORT)
