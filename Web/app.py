import numpy
import scipy
import sklearn
from flask import Flask, render_template,  make_response
import wbdata
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components 
from bokeh.palettes import Spectral11
from bokeh.charts import TimeSeries, show, output_file, Bar
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.charts.utils import df_from_json

app = Flask(__name__)

@app.route("/plot1")
def plot1():
    return render_template('plot1.html')

@app.route('/plot2') 
def plot2():
	p = figure(title='Data from worldbank.org (SH.H2O.SAFE.ZS)',
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
	               title="", ylabel='Improved water source (% of population)')
	
	script, div = components(p)
	return render_template('plot2.html', script=script, div=div)

@app.route("/plot3")
def plot3():
	plot = figure(title='',
              x_axis_label='date',
              x_axis_type='datetime')
	df=pd.read_csv('chart.csv')
	df = df[df['status'] =='water consumer']
	df1=df[['Population possible access National water','Name']]
	df1.columns=['Population wo access water','Name']
	df1['category']='Population possible access National water'
	df2=df[['Revised Pop wo water','Name']]
	df2.columns=['Population wo access water','Name']
	df2['category']='Revised Pop wo water'
	df3=pd.concat([df1,df2])

	p=Bar(df3,label='Name',values='Population wo access water',stack='category',legend='top_right')
	output_file("stacked_bar.html")	
	script, div = components(plot)
	return render_template('plot3.html', script=script, div=div)

if __name__ == "__main__":
    app.run(debug=True)