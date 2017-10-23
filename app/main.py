from bokeh.plotting import figure
import bokeh.events
import bokeh.models
from bokeh.models.callbacks import CustomJS
from bokeh.embed import components
from bokeh.resources import INLINE
from jinja2 import Template
import numpy as np
import json

x, t = np.arange(-10,11), np.arange(-10,11)
y = np.array([x**2]*21) - np.array([t**3]).T 

x,t,y = x.tolist(), t.tolist(), y.tolist()
absolute_value_domain = np.abs(x).tolist()

bokeh_tools =["pan", "wheel_zoom", "box_select", "lasso_select"]

template = Template('''
<html>
    <head>
        <meta charset="utf-8">
        <title></title>
        {{ js_resources }}
        {{ css_resources }}
        <script>function update_time_slice(t){var xhttp = new XMLHttpRequest();xhttp.open("POST", "edit_source_data", true);xhttp.setRequestHeader("Content-type", "application/JSON");xhttp.send(JSON.stringify({time_slice:t}));}</script>
    </head>
    <body>
    Time Slice:
    <input type="range" min="-10" max="10" value="0" step="1" onchange="update_time_slice(this.value);">
    <br>
    {{ plot_div }}
    {{ plot_script }}
    </body>
<script>
window.addEventListener("load", function(){
	Array.from(document.getElementsByClassName('bk-bs-btn bk-bs-btn-default')).filter(x=>x.innerHTML=='delete_me_onload').map(x=>x.click());
	Array.from(document.getElementsByClassName('bk-bs-btn bk-bs-btn-default')).filter(x=>x.innerHTML=='delete_me_onload').map(x=>x.parentElement.parentElement.remove());
});
</script>
</html>
''')

def get_data(time_slice):
	return {'y': y[time_slice+10],
			'domain': x,
			'absolute_value': absolute_value_domain}


def get_html(source):
	# attach selection reaction - this should not be changed
	source.callback = CustomJS(args={}, code="BOKEH_GLOBALS.fns.selection_reaction();")
	# define plots
	absolute_plot = figure(tools=bokeh_tools)
	absolute_plot.scatter('domain', 'absolute_value', source=source)
	saddle_plot = figure(tools=bokeh_tools)
	saddle_plot.scatter('domain', 'y', source=source)
	# define auxiliary variables
	js_aux_vars = {'favorite_name': 'Foo', 'favorite_color': [255, 0, 0]}
	js_aux_vars = json.dumps(js_aux_vars)
	# define initialization - this should not be changed
	js_initialization = open("app/js_assets.js").read()
	js_initialization += '''initialize_BOKEH_GLOBALS(source, \''''+js_aux_vars+'''\');'''
	js_initialization = CustomJS(args={'source': source}, code=js_initialization)
	# make something trigger init - this should be improved.  Ideally, the trigger would be an onload event
	trigger = bokeh.models.Button(label="delete_me_onload")
	trigger.js_on_click(js_initialization)
	# make layout
	layout = (trigger, saddle_plot, absolute_plot)
	script, div = components(layout, INLINE)
	html = template.render(
		plot_script=script,
		plot_div=div,
		js_resources=INLINE.render_js(),
		css_resources=INLINE.render_css())
	return html
