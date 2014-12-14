from flask import Flask, render_template

# Note: it is ugly that this imports "conn" directly as a symbol.
# The initialization of that stuff should not be hidden in that module.
from persistence_layer.pers_layer import *

app = Flask(__name__)
 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/violations")
def violations():
    return render_template("violations.html")
    
@app.route("/employees")
def employees():
    return render_template("employees.html")

@app.route("/employeesx")
def employeesxs():
    case_id = 7049;
    emps = read_employees_from_case(conn,case_id)
    print emps
    return render_template("employeesx.html",case_id=case_id,employees=emps)
    
@app.route("/manual")
def manual():
    return render_template("manual.html")

# not a typo
@app.route("/import")
def iimport():
    return render_template("import.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
