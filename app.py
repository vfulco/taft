from flask import Flask, redirect, render_template, request, send_file
from flask_sslify import SSLify
app = Flask(__name__)
sslify = SSLify(app)

import docxstache.docxstache as docxstache
import json
import os
import uuid

def convert(docx_f, json_f):
    # with open(json_f) as f:
    o = json.loads(json_f.read())
    fname = os.path.join(os.getcwd(), 'files', str(uuid.uuid4()) + ".docx")
    docx = docx_f.save(fname)
    return docxstache.replace_document(fname, o)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        docx_file = request.files["docx_file"]
        json_file = request.files["json_file"]
        # print convert(docx_file, json_file)
        doc = convert(docx_file, json_file)
        fname = 'files/' + str(uuid.uuid4()) + ".docx"
        response = doc.save(fname)
        return send_file(fname, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    return render_template('index.html')

app.debug = False
if __name__ == '__main__':
    app.run()