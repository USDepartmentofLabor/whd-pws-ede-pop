from flask import Flask, render_template


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