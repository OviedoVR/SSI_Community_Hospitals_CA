import plotly.express as px

# Define a custom layout dictionary
custom_layout = {
    #'width': 700,
    #'height': 400,
    'paper_bgcolor': 'white',
    'plot_bgcolor': 'white',
    'font': {'family': 'Palatino', 'size': 12},
    'xaxis_showgrid': False,
    'yaxis_showgrid': False,
    #'xaxis_linecolor': 'lightgray',
    #'yaxis_linecolor': 'lightgray',
    'xaxis_zeroline': False,
    'xaxis': {
        'showline': True,
        #'tickfont': {'color': 'lightgray'}  # Change tick font color to light gray
    },
    'yaxis': {
        #'tickfont': {'color': 'lightgray'}  # Change tick font color to light gray
    }
}

# Set the default template:
px.defaults.template = 'simple_white'

# Defining a color palette:
#px.defaults.color_discrete_sequence =  ['#bdbf09', '#2292a4', '#373F51', '#CE4760', '#d96c06']

# Create a custom marker style dictionary
custom_marker_style = {
    'size': 14,
    'opacity': 0.75,
    'line': {'width': 1, 'color': 'black'}
}