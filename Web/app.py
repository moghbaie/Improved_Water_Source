import numpy
import scipy
import sklearn
from flask import Flask, render_template,  make_response

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')

if __name__ == '__main__':
    # Use this port=33507 when you want to Flask to work on Heroku....
    app.run()
