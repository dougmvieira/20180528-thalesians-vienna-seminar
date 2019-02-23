import bokeh.io
import bokeh.models
import bokeh.plotting
import bokeh.layouts
import bokeh.embed
import bokeh.resources
import pandas as pd
import numpy as np


tick_size = 1/8

sp500 = pd.concat([pd.read_pickle('prices.pickle')], axis=1, keys=['Price'])
heston = pd.read_pickle('simulation.pickle')
rounded_heston = tick_size*np.round(heston[['Price']]/tick_size, 0)

bokeh_sp500 = bokeh.models.ColumnDataSource(sp500)
bokeh_heston = bokeh.models.ColumnDataSource(heston)
bokeh_rounded_heston = bokeh.models.ColumnDataSource(rounded_heston)


# S&P 500 futures

p = bokeh.plotting.figure(plot_height=400, x_axis_type="datetime",
                          y_range=(sp500['Price'].min(), sp500['Price'].max()),
                          x_range=(sp500.index[0], sp500.index[-1]),
                          x_axis_label='Time',
                          y_axis_label='S&P 500 futures price',
                          sizing_mode="stretch_both")
s = p.step(y='Price', x='Time', source=bokeh_sp500)

callback = bokeh.models.CustomJS(args=dict(xr=p.x_range, yr=p.y_range,
                                           src=s.data_source), code="""
var m = cb_obj.value;
var t = src.data['Time'];
var y = src.data['Price'];

xr.end = t[0] + (t[t.length - 1] - t[0])/Math.pow(10.0, m);
xr.change.emit();

var mask = t.map(el => el < xr.end);
var sel_ys = y.filter((item, i) => mask[i]);

yr.start = Math.min.apply(null, sel_ys);
yr.end = Math.max.apply(null, sel_ys);
yr.change.emit();
""")
slider = bokeh.models.widgets.Slider(start=0, end=6, value=0, step=0.1,
                                     title="Zoom magnitude")
slider.js_on_change('value', callback)

html = bokeh.embed.file_html([p, slider], bokeh.resources.CDN)
with open('20180528/sp500.html', 'w') as f:
    f.write(html)


# Heston simulation

p1 = bokeh.plotting.figure(plot_height=200, x_axis_type="datetime",
                           y_range=(heston['Price'].min(),
                                    heston['Price'].max()),
                           x_range=(heston.index[0], heston.index[-1]),
                           y_axis_label='Simulated price',
                           sizing_mode="stretch_both")
p2 = bokeh.plotting.figure(plot_height=200, x_axis_type="datetime",
                           y_range=(heston['Vol'].min(),
                                    heston['Vol'].max()),
                           x_range=(heston.index[0], heston.index[-1]),
                           x_axis_label='Time',
                           y_axis_label='Simulated volatilty',
                           sizing_mode="stretch_both")
s = p1.step(y='Price', x='Time', source=bokeh_heston)
s = p2.step(y='Vol', x='Time', source=bokeh_heston)

callback = bokeh.models.CustomJS(args=dict(xr1=p1.x_range, yr1=p1.y_range,
                                           xr2=p2.x_range, yr2=p2.y_range,
                                           src=s.data_source), code="""
var m = cb_obj.value;
var t = src.data['Time'];
var y1 = src.data['Price'];
var y2 = src.data['Vol'];

xr1.end = t[0] + (t[t.length - 1] - t[0])/Math.pow(10.0, m);
xr2.end = t[0] + (t[t.length - 1] - t[0])/Math.pow(10.0, m);
xr1.change.emit();
xr2.change.emit();

var mask = t.map(el => el < xr1.end);
var sel_ys1 = y1.filter((item, i) => mask[i]);
var sel_ys2 = y2.filter((item, i) => mask[i]);

yr1.start = Math.min.apply(null, sel_ys1);
yr1.end = Math.max.apply(null, sel_ys1);
yr1.change.emit();
yr2.start = Math.min.apply(null, sel_ys2);
yr2.end = Math.max.apply(null, sel_ys2);
yr2.change.emit();
""")
slider = bokeh.models.widgets.Slider(start=0, end=6, value=0, step=0.1,
                                     title="Zoom magnitude")
slider.js_on_change('value', callback)

combined = bokeh.layouts.column(p1, p2, sizing_mode="stretch_both")
html = bokeh.embed.file_html([combined, slider], bokeh.resources.CDN)
with open('20180528/heston.html', 'w') as f:
    f.write(html)


# Rounded Heston

p = bokeh.plotting.figure(plot_height=400, x_axis_type="datetime",
                          y_range=(rounded_heston['Price'].min(),
                                   rounded_heston['Price'].max()),
                          x_range=(rounded_heston.index[0],
                                   rounded_heston.index[-1]),
                          x_axis_label='Time',
                          y_axis_label='Simulated prices',
                          sizing_mode="stretch_both")
s = p.step(y='Price', x='Time', source=bokeh_rounded_heston)

callback = bokeh.models.CustomJS(args=dict(xr=p.x_range, yr=p.y_range,
                                           src=s.data_source), code="""
var m = cb_obj.value;
var t = src.data['Time'];
var y = src.data['Price'];

xr.end = t[0] + (t[t.length - 1] - t[0])/Math.pow(10.0, m);
xr.change.emit();

var mask = t.map(el => el < xr.end);
var sel_ys = y.filter((item, i) => mask[i]);

yr.start = Math.min.apply(null, sel_ys);
yr.end = Math.max.apply(null, sel_ys);
yr.change.emit();
""")
slider = bokeh.models.widgets.Slider(start=0, end=6, value=0, step=0.1,
                                     title="Zoom magnitude")
slider.js_on_change('value', callback)

html = bokeh.embed.file_html([p, slider], bokeh.resources.CDN)
with open('20180528/rounded_heston.html', 'w') as f:
    f.write(html)
