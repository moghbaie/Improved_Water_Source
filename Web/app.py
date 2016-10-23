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
	countries = ["CL","UY","HU"] 
	indicators = {'SH.H2O.SAFE.ZS':'Improved water source'}
	df = wbdata.get_dataframe(indicators, country=countries, convert_date=False)
	dfu = df.unstack(level=0)

	plotPng = dfu.plot(); 
	plt.legend(loc='best'); 
	plt.title("Improved water source (% of population)"); 
	plt.xlabel('Date'); plt.ylabel('Improved water source (% of population');
# if __name__ == '__main__':
#     # Use this port=33507 when you want to Flask to work on Heroku....
#     app.run()
if __name__ == "__main__":
    app.run(debug=True)