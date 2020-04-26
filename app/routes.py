from app import app
from flask import render_template

import boto3


@app.route('/')
@app.route('/index')
def index():

    message = "Hey there, welcome to my website."
    return render_template("index.html", message=message)

@app.route('/readme')
def readme():
    message = "Welcome to the readme page"
    return render_template("readme.html", message=message)

@app.route('/about')
def about():
    message = "About Catland"
    return render_template("about.html", message=message)

@app.route('/db')
def db():

    dynamobd = boto3.resource('dyanamobd',region_name= 'us-west-2', endpoint_url="http://localhost:8000")

    table = dynamobd.create.table(
        TableName= 'Uploadedpictures',
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
            },
            {
                'AttributeName': 'originalLocation',
                'KeyType': 'HASH'
            },

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
            'AttributeType': 'N'
            },
            {
            'AttributeName': 'Filesize',
            'AttributeType': 'N'
            },
            {
            'AttributeName': 'originalLocation',
            'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Table status:", table.table_status)