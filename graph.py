from bokeh.models.callbacks import CustomJS
from bokeh.layouts import grid, column, row
from bokeh.models.widgets import Select, Button
from bokeh.plotting import figure, output_file, show
from bokeh.events import ButtonClick

output_file('dashboard.html')

def callback(event):
    print('Python:Click')

def controls():
    options = ["item 1", "item 2", "item 3"]
    firstSignal = Select(title="First signal:", options=options)
    secondSignal = Select(title="Second signal:", options=options)
    findButton = Button(label="Find similarities", button_type="success")
    findButton.on_event(ButtonClick, callback)
    widgets = column(firstSignal, secondSignal, findButton)

    return widgets


def plotter():
    x = [-3, 2, -1, 1]
    y =  [-1, 0, -3, 2]

    x1 = [-5, 3, -2, 1]
    y1 = [-4, 4, -2, 1]

    plot1 = figure(
        y_range=(-5, 5), title="First signal", width=1250, height=350
    )
    plot1.line(x, y)

    callback = CustomJS(code="""
    console.log('Tap event occurred at x-position: ' + cb_obj.x)
    """)
    plot1.js_on_event('doubletap', callback)

    plot2 = figure(
        y_range=(-5, 5), title="Second signal", width=1250, height=350
    )
    plot2.line(x1, y1)
    plots = column(plot1, plot2)
    return plots


l = row(controls(), plotter())
show(l)