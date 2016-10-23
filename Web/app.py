import numpy
import scipy
import sklearn
from flask import Flask, render_template,  make_response
import wbdata
import pandas
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route('/plot')
def plot():
	return render_template('echo.html')
# if __name__ == '__main__':
#     # Use this port=33507 when you want to Flask to work on Heroku....
#     app.run()
if __name__ == "__main__":
    app.run(debug=True)