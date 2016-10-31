import numpy
from flask import Flask, render_template,  make_response
import wbdata
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components 
from bokeh.palettes import Blues9
from bokeh.charts import TimeSeries, show, output_file, Bar
from bokeh.charts.attributes import cat, color


app = Flask(__name__)

@app.route("/plot1")
def plot1():
    return render_template('plot1.html')

@app.route('/plot2') 
def plot2():
	p = figure(title='Data from worldbank.org (SH.H2O.SAFE.ZS)',
	              x_axis_label='date',
	              x_axis_type='datetime')
	countries = ['AF','TZ','AO','MG','MZ','CG']
	indicators = {'SH.H2O.SAFE.ZS':'Improved water source'}
	df1 = wbdata.get_dataframe(indicators, country=countries, convert_date=False)
	indicators2 = {'SP.POP.TOTL':'Total Population'}
	df2 = wbdata.get_dataframe(indicators2, country=countries, convert_date=False)
	dfu1 = df1.unstack(level=0)
	dfu1=dfu1['1990':]
	dfu2 = df2.unstack(level=0)
	dfu2=dfu2['1990':]
	dfu=pd.DataFrame(dfu1.values*dfu2.values,columns=dfu1.columns, index=dfu1.index)
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
		# New_Guinea=dfu[6],
		# Saudi_Arabia=dfu[7],
		# Chad=dfu[8],
		# Mongolia=dfu[9],
	        Date=dfu['Date']
	    ))

	output_file("stocks_timeseries.html")

	p = TimeSeries(xyvalues, x='Date', legend=True,
	               title="", ylabel='Population with no access to improved source of water')
	
	script, div = components(p)
	return render_template('plot2.html', script=script, div=div)

@app.route("/plot3")
def plot3():
	p = figure(title='something',
              x_axis_label='date',
              x_axis_type='datetime')
	df=pd.read_csv('chart.csv')
	df3=pd.read_csv('df3d.csv')
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