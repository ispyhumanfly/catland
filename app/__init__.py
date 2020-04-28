from flask import Flask
app = Flask(__name__, static_url_path="/", static_folder="/assets")

app.config['UPLOAD_FOLDER'] = './uploads'
app.config['SECRET_KEY'] = 'the random string'    

from app import routes
