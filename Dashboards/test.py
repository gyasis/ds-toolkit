# %%
import hvplot.pandas
from bokeh.sampledata.autompg import autompg

def autompg_plot(x='mpg', y='hp', color='#058805'):
    return autompg.hvplot.scatter(x, y, c=color, padding=0.1)

columns = list(autompg.columns[:-2])
# %%
autompg_plot()
# %%
#IMPORTANT!!!!!!!!!!!!!!!!! the following is the code for the interactive plot
import panel as pn
pn.extension(comms='vscode')

# %%
color = pn.widgets.ColorPicker(name='Color', value='#4f4fdf')
layout = pn.interact(autompg_plot, x=columns, y=columns, color=color)

pn.Row(pn.Column('## MPG Explorer', layout[0]), layout[1])
# %%
def fn(a,b): return f'Arguments: {a,b}'
slider = pn.widgets.FloatSlider(value=0.5)

bound_fn = pn.bind(fn, a=slider, b=2)
bound_fn()
# %%
pn.Row(slider, bound_fn)
# %%
x = pn.widgets.Select(value='mpg', options=columns, name='x')
y = pn.widgets.Select(value='hp', options=columns, name='y')
color = pn.widgets.ColorPicker(name='Color', value='#AA0505')

pn.Row(pn.Column('## MPG Explorer', x, y, color),
       pn.bind(autompg.hvplot.scatter, x, y, c=color))
# %%





x = pn.widgets.Select(value='mpg', options=columns, name='x')
y = pn.widgets.Select(value='hp', options=columns, name='y')
color = pn.widgets.ColorPicker(name='Color', value='#880588')

layout = pn.Row(
    pn.Column('## MPG Explorer', x, y, color),
    autompg_plot(x.value, y.value, color.value))

def update(event):
    layout[1].object = autompg_plot(x.value, y.value, color.value)

x.param.watch(update, 'value')
y.param.watch(update, 'value')
color.param.watch(update, 'value')

layout
# %%
