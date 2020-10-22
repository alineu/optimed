import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



# We `import os` and use the os.environ method to import the appropriate `APP_SETTINGS`
# variables, depending on our environment. We then set up the config in our app
# with the `app.config.from_object` method.

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
