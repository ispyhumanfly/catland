from flask import Flask
app = Flask(__name__, static_url_path="/", static_folder="/assets")
app.config['UPLOAD_FOLDER'] = "."

from app import routes 