from flask import Flask, render_template

# Note: it is ugly that this imports "conn" directly as a symbol.
# The initialization of that stuff should not be hidden in that module.
from persistence_layer.pers_layer import *

from functools import wraps
from flask import request, Response
import os


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == os.environ['FLASK_USERNAME'] and password == os.environ['FLASK_PASSWORD']

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

def pretty(e):
    return "<p>"+e[0]+","+e[2]+" "+e[1]+"."+"</p>"

app = Flask(__name__)
 


@app.route("/")
@requires_auth
def index():
    return render_template("index.html")

@app.route("/violations")
@requires_auth
def violations():
    return render_template("violations.html")
    
@app.route("/employeesx")
@requires_auth
def employeesx():
    emps = get_employee_names()
    return "\n".join(map(pretty,emps))
    return render_template("employees.html")

@app.route("/employees")
@requires_auth
def employees():
    case_id = find_random_case(conn)
    emps = read_employees_from_case(conn,case_id)
    print emps
    return render_template("employeesx.html",case_id=case_id,employees=emps)

@app.route("/add_employee")
@requires_auth
def add_employee():
    f = request.args.get('fname')
    m = request.args.get('mname')
    m = m[0]
    l = request.args.get('lname')
    case_id = request.args.get('case_id',0,type=int)
    print f + m + l + " into case: "+str(case_id)
    create_new_employee(conn,case_id,f,m,l)
    return f + m + l + " into case: "+str(case_id)

    
@app.route("/manual")
@requires_auth
def manual():
    return render_template("manual.html")

# not a typo
@app.route("/import")
@requires_auth
def iimport():
    return render_template("import.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
