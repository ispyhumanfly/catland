from app import app

from flask import render_template, request, redirect, flash, session, url_for, abort, safe_join, send_file, send_from_directory
from werkzeug.utils import secure_filename

import boto3
import botocore

import os


@app.route('/')
@app.route('/index')
def index():
    message = "Hey there, welcome to my website."
    return render_template("index.html", message=message)


@app.route('/bootstrap')
def bootsrap():
    message = "Welcome to the bootstrap page."
    return render_template("bootstrap.html", message=message)


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

    images = []

    client = boto3.client('s3')

    for file in client.list_objects(Bucket='catland-uploads')['Contents']:
        url = "/download/%s" % (file['Key'])
        images.append(url)
        print(url)

    return render_template('gallery.html', message=message, images=images)


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

            s3 = boto3.resource('s3')
            s3.meta.client.upload_file(os.path.join(
                app.config['UPLOAD_FOLDER'], filename), 'catland-uploads', filename)

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
        # TODO start saving files temporarily in ./tmp instead of ./uploads...
        s3.Bucket("catland-uploads").download_file(filename,
                                                   "./app/uploads/%s" % filename)
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=filename, as_attachment=False)
    except:
        print("something went wong")

    safe_path = safe_join(app.config["UPLOAD_FOLDER"], filename)

    return send_file("uploads", filename)
    # return send_from_directory("./uploads", filename=filename)
