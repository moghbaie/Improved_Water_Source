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
	plot = figure(title='something',
              x_axis_label='date',
              x_axis_type='datetime')
	df=pd.read_csv('chart.csv')
	dfd = df[df['status'] =='water consumer']
	df1=dfd[['Population possible access National water','Country']]

	df1.columns=['Population wo access water','Country']
	df1['category']='Population possible access National water'

	df2=dfd[['Revised Pop wo water','Country']]
	df2.columns=['Population wo access water','Country']
	df2['category']='Revised Pop wo water'
	df3=pd.concat([df1,df2])
	output_file("stacked_bar.html")
	p=Bar(df3,label='Country',values='Population wo access water',stack='category',
		color=color(columns='category', palette=['Orange','Red'],
                      sort=False),legend='top_right')

	script, div = components(p)
	df4= df[df['status'] =='water supplier']
	output_file("bar.html")
	q=Bar(df4,label='Country',values='Possible water provider',legend=False, color="Green")
	script2, div2 = components(q)
	return render_template('plot3.html', script=script, div=div, script2=script2, div2=div2)

if __name__ == "__main__":
    app.run(debug=True)