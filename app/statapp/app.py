from flask import Flask
from flask_wtf.csrf import CSRFProtect

application = Flask(__name__)
application.secret_key = "aslkdja8901d"
csrf = CSRFProtect(application)


