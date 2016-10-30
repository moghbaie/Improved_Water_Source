import numpy
import scipy
import sklearn
from flask import Flask, render_template,  make_response
import wbdata
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components 
from bokeh.palettes import Spectral11
from bokeh.charts import TimeSeries, show, output_file

app = Flask(__name__)

@app.route("/plot1")
def hello():
    return render_template('hello.html')

@app.route('/plot2')
def plot():
	p = figure(title='Improved water source % of population',
	              x_axis_label='date',
	              x_axis_type='datetime')
	countries = ['AF','TZ','AO','MG','MZ','CG','PG','SA','TD','MN']
	indicators = {'SH.H2O.SAFE.ZS':'Improved water source'}
	df = wbdata.get_dataframe(indicators, country=countries, convert_date=False)
	dfu = df.unstack(level=0)
	dfu=dfu['1990':]
	range(dfu.shape[1])
	dfu.columns=range(dfu.shape[1])
	dfu['Date']=dfu.index
	xyvalues = pd.DataFrame(dict(
		Afghanistan=dfu[0],
		Tanzania=dfu[1],
		Angola=dfu[2],
		Madagascar=dfu[3],
		Mozambique=dfu[4],
		Congo=dfu[5],
		New_Guinea=dfu[6],
		Saudi_Arabia=dfu[7],
		Chad=dfu[8],
		Mongolia=dfu[9],
	        Date=dfu['Date']
	    ))

	output_file("stocks_timeseries.html")

	p = TimeSeries(xyvalues, x='Date', legend=True,
	               title="Water Source", ylabel='Improved water source (% of population)')
	
	script, div = components(p)
	return render_template('echo.html', script=script, div=div)


# if __name__ == '__main__':
#     # Use this port=33507 when you want to Flask to work on Heroku....
#     app.run()
if __name__ == "__main__":
    app.run(debug=True)