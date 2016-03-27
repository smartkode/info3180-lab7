from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'GGSB216737128edsgudsgdf #$$%^&89WEG{UDF}'
app.config['UPLOAD_FOLDER'] = "app/static"

from app import views
