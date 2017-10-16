from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.callbacks import CustomJS
import bokeh
import json

# define columns
domain = [x for x in range(-10,11)]
absolute = [abs(x) for x in domain]
squared = [x**2 for x in domain]

# define source
source = {'domain': domain, 'absolute': absolute, 'squared': squared}
source = ColumnDataSource(data=source)

# attach selection reaction - this should not be changed
source.callback = CustomJS(args={}, code="BOKEH_GLOBALS.fns.selection_reaction();")

# define auxiliary variables
js_aux_vars = {'favorite_name': 'Foo', 'favorite_color': [255, 0, 0]}
js_aux_vars = json.dumps(js_aux_vars)

# define initialization - this should not be changed
js_initialization = open("js_assets.js").read()
js_initialization += '''initialize_BOKEH_GLOBALS(source, \''''+js_aux_vars+'''\');'''
js_initialization = CustomJS(args={'source': source}, code=js_initialization)

# define tools and plots
tools =["pan", "wheel_zoom", "box_select", "lasso_select"]

absolute_plot = figure(tools=tools)
absolute_plot.scatter('domain', 'absolute', source=source)

squared_plot = figure(tools=tools)
squared_plot.scatter('domain', 'squared', source=source)

# make something trigger init - John, this should be improved.  Ideally, the trigger would be an onload event
absolute_plot.js_on_event(bokeh.events.MouseMove, js_initialization)

# show
output_file("demo.html", title="Multi Window Demo")
show(bokeh.layouts.row(absolute_plot, squared_plot))
