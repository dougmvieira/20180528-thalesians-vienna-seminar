import jinja2
import bokeh.io
import bokeh.models
import bokeh.plotting
import bokeh.layouts
import bokeh.embed
import bokeh.resources
import pandas as pd
import numpy as np

np.random.seed(42)
n = 18
side_color = {'Bid': ['#1f77b4', '#aec7e8'], 'Ask': ['#ff7f0e', '#ffbb78']}

times = pd.Series(pd.to_datetime('9:00:00')
                  + pd.to_timedelta(np.arange(n), unit='s'), name='Time')
sizes = pd.Series(1 + np.random.poisson(0.75, n), name='Size')
prices = pd.Series(96 + np.random.binomial(7, 0.5, n), name='Price')
side = pd.Series(['Bid' if p < 100 else 'Ask' for p in prices], name='Side')

lob = pd.concat([side, times, prices, sizes], axis=1)
lob_ask = lob[lob['Side']=='Ask']
lob_bid = lob[lob['Side']=='Bid']
lob_ask.sort_values(['Price', 'Time'], ascending=[False, False], inplace=True)
lob_bid.sort_values(['Price', 'Time'], ascending=[True, False], inplace=True)
lob = pd.concat([lob_ask, lob_bid])
lob.reset_index(inplace=True)
lob['Cumulative Size'] = lob[['Price', 'Size']].groupby('Price').transform(
    lambda x: np.cumsum(x.iloc[::-1]).iloc[::-1])
lob['Color'] = lob[['Price', 'Side']].groupby('Price').transform(
    lambda x: (int(len(x)/2 + 1)*side_color[x.iloc[0]])[:len(x)])
lob['Time'] = lob['Time'].dt.strftime('%H:%M:%S')

source = bokeh.models.ColumnDataSource(data=lob)
fig = bokeh.plotting.figure(sizing_mode="stretch_both")
fig.vbar(x='Price', top='Cumulative Size', width=0.9, fill_color='Color',
         source=source)

columns_widths = [('Side', 0), ('Time', 40), ('Price', 0), ('Size', 0)]
bokeh_columns = [bokeh.models.widgets.TableColumn(
    field=col, title=col, width=width) for col, width in columns_widths]
data_table = bokeh.models.widgets.DataTable(
    columns=bokeh_columns, index_position=None, sizing_mode="stretch_both",
    height=500, fit_columns=True, source=source)

combined = bokeh.layouts.row(fig, data_table, sizing_mode="stretch_both")

with open('bokeh_template.jinja', 'r') as f:
    template = jinja2.Template(f.read())
html = bokeh.embed.file_html(combined, bokeh.resources.CDN, template=template)

with open('20180528/lob.html', 'w') as f:
    f.write(html)
