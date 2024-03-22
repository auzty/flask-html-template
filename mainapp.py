import os,secrets
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import pandas as pd
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/upload", methods=['POST'])
def uploadFiles():

    if 'fname' not in request.files:
        return {'msg': 'File Not Found'},400

    file = request.files['fname']

    if file and allowed_file(file.filename):

        filename = file.filename

        # init the fullpath variable
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        # save file to path
        file.save(fullpath)

        # Processing the CSV
        result = processCSV(fullpath)

        # return data to client
        return render_template('index.html',data=result)

def processCSV(path):
    df = pd.read_csv(path,sep=',')
    return df.loc[:,'Salary'].mean()

if __name__ == '__main__':
   app.run()