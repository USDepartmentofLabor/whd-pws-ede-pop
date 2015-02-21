from flask import Flask
from pers_layer import *
from functools import wraps
from flask import request, Response
import os

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'investigator' and password == 'untothislast'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


app = Flask(__name__)

app.config.update(
    DEBUG=True
)

@app.route("/")
@requires_auth
def hello():
    return "Hello World!"

def pretty(e):
    return "<p>"+e[0]+","+e[2]+" "+e[1]+"."+"</p>"

@app.route("/employee")
@requires_auth
def employee():
    emps = get_employee_names()
    return "\n".join(map(pretty,emps))

if __name__ == "__main__":
    app.run()
