from app import app

from flask import render_template, request, redirect, flash, session, url_for, abort, safe_join, send_file, send_from_directory
from werkzeug.utils import secure_filename
from postmark.core import PMMail

import boto3
import botocore
import tempfile
import os


@app.route('/')
@app.route('/index')
def index():
    message = "Hey there, welcome to my website."

    images = []

    client = boto3.client('s3')

    for file in client.list_objects(Bucket='catland-uploads')['Contents']:
        url = "/download/%s" % (file['Key'])
        images.append(url)
        print(url)

    return render_template("index.jinja", message=message, images=images)


@app.route('/bootstrap')
def bootsrap():
    message = "Welcome to the bootstrap page."
    return render_template("bootstrap.jinja", message=message)


@app.route('/readme')
def readme():
    message = "Welcome to the readme page."
    return render_template("readme.jinja", message=message)


@app.route('/about')
def about():
    message = "About Catland"
    return render_template("about.jinja", message=message)


@app.route('/gallery')
def gallery():
    message = "Gallery"

    images = []

    client = boto3.client('s3')

    for file in client.list_objects(Bucket='catland-uploads')['Contents']:
        url = "/download/%s" % (file['Key'])
        images.append(url)
        print(url)

    return render_template('gallery.jinja', message=message, images=images)


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():

    message = "Uploader"

    client = boto3.client('s3')

    try:
        response = client.create_bucket(
            ACL='public-read-write',
            Bucket='catland-uploads',
            CreateBucketConfiguration={
                'LocationConstraint': 'us-east-2'
            }
        )
    except:
        print("The bucket existed already, move along...")

    if request.method == 'GET':
        return render_template('uploader.jinja', message=message)
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
            file.save(os.path.join(tempfile.gettempdir(), filename))

            s3 = boto3.resource('s3')
            s3.meta.client.upload_file(os.path.join(
                tempfile.gettempdir(), filename), 'catland-uploads', filename)

            bucket = s3.Bucket('catland-uploads')

            for file in bucket.objects.all():
                print(file.key)

            conn = client('s3')
            for key in conn.list_objects(Bucket='catland-uploads')['Contents']:
                print(key['Key'])

            return redirect(url_for('uploader', filename=filename))


@app.route('/download/<filename>')
def download(filename):
    s3 = boto3.resource("s3")

    try:
        s3.Bucket("catland-uploads").download_file(filename,
                                                   os.path.join(tempfile.gettempdir(), filename))
    except:
        print("something went wrong")

    return send_file(os.path.join(tempfile.gettempdir(), filename))


@app.route('/contact')
def contact():

    pm = PMMail(api_key="0e1604ec-e20c-438f-b7c0-3ea34878b849", to='mcbryankim@gmail.com', sender='harpo.marx@gmail.com',
                template_id=17926943, template_model={
                    'name': 'Bob',
                    'product_name': 'Catland',
                    'login_url': 'meow moew',
                    'username': 'Meow cat',
                    'trial_start': '358357',
                    'trial_end': '5767373',
                    'sender_name': 'Kim'
                })

    pm.send()
