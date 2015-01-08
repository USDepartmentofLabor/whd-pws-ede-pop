from flask import Flask
from pers_layer import *


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def pretty(e):
    return "<p>"+e[0]+","+e[2]+" "+e[1]+"."+"</p>"

@app.route("/employee")
def employee():
    emps = get_employee_names()
    return "\n".join(map(pretty,emps))

if __name__ == "__main__":
    app.run()
