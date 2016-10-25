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

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route('/plot')
def plot():
	p = figure(title='Improved water source % of population',
	              x_axis_label='date',
	              x_axis_type='datetime')
	countries = ["BR","ES","PT","ZA","CD","LY","ML","MR","NE","NG","TD"]
	indicators = {'SH.H2O.SAFE.ZS':'Improved water source'}
	df = wbdata.get_dataframe(indicators, country=countries, convert_date=False)
	dfu = df.unstack(level=0)
	dfu=dfu['1990':]
	range(dfu.shape[1])
	dfu.columns=range(dfu.shape[1])
	dfu['Date']=dfu.index
	xyvalues = pd.DataFrame(dict(
	        Brazil=dfu[0],
	        Chad=dfu[1],
	        Congo=dfu[2],
	        Libya=dfu[3],
	        Mali=dfu[4],
	        Mauritania=dfu[5],
	        Niger=dfu[6],
	        Nigeria=dfu[7],
	        Portugal=dfu[8],
	        SouthAfrica=dfu[9],
	        Spain=dfu[10],
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