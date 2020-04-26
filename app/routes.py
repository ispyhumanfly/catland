from app import app
from flask import render_template, request, redirect, flash
from werkzeug.utils import secure_filename

import boto3

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
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