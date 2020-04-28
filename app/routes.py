from app import app

from flask import render_template, request, redirect, flash, session, url_for, send_from_directory
from werkzeug.utils import secure_filename

import boto3
import os

@app.route('/')
@app.route('/index')
def index():
    message = "Hey there, welcome to my website."
    return render_template("index.html", message=message)

@app.route('/readme')
def readme():
    message = "Welcome to the readme page."
    return render_template("readme.html", message=message)

@app.route('/about')
def about():
    message = "About Catland"
    return render_template("about.html", message=message)

@app.route('/gallery')
def gallery():
    message = "Gallery"
    return render_template('gallery.html', message=message)

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    message = "Uploader"

    if request.method == 'GET':
        return render_template('uploader.html', message=message)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploader',
                                    filename=filename))

@app.route('/db')
def db():

    dynamobd = boto3.resource('dyanamobd',region_name= 'us-east-2', endpoint_url="http://localhost:5000")

    table = dynamobd.create.table(
        TableName= 'Gallery',
        KeySchema=[
            {
                'AttributeName': 'ID',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Timestamp',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Filename',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Filesize',
                'KeyType': 'HASH'
            }

        ],
        AttributeDefinition=[
            {
            'AttributeName': 'ID',
            'AttributeType': 'N'
            },
            {
            'AttributeName': 'Timestamp',
            'AttributeType': 'N'
            },
            {
            'AttributeName': 'Filename',
            'AttributeType': 'S'
            },
            {
            'AttributeName': 'Filesize',
            'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Table status:", table.table_status)

# Static Directory Services

@app.route('/styles/<path:path>')
def send_js(path):
    return send_from_directory('styles', path)

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)