# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # JupyterDash
# The `jupyter-dash` package makes it easy to develop Plotly Dash apps from the Jupyter Notebook and JupyterLab.
#
# Just replace the standard `dash.Dash` class with the `jupyter_dash.JupyterDash` subclass.

# %%
#from jupyter_dash import JupyterDash

# %%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc
import datetime
import webbrowser

url = 'http://127.0.0.1:8050'
webbrowser.open_new(url)

# %% [markdown]
# When running in JupyterHub or Binder, call the `infer_jupyter_config` function to detect the proxy configuration.

# %%
#JupyterDash.infer_jupyter_proxy_config()

# %% [markdown]
# Load and preprocess data

# %%
df = pd.read_csv('FarmData.csv')
#available_indicators = df['PondLevel'].unique()

# %% [markdown]
# Construct the app and callbacks

# %%

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Create server variable with Flask server object for use with gunicorn
server = app.server

app.layout = html.Div([
    dbc.Container([
    html.Img(src='/assets/Background.png', style={'width':'60%'}),
    dbc.Jumbotron([
    html.H1("Farm Pond Levels", className="display-3"),
    html.P("Hover mouse on line to see values.", className="lead"),
    html.P("Click tabs to change dates shown.", className="lead"),
    html.P("Double click anywhere in the graph to reset zoom.", className="lead"),
    ], fluid=True,)],
    fluid=True,
    ),
    dcc.Graph(id="graph"),
    dcc.RadioItems(
        id='radio',
        value='Secondary',
    ),
    dbc.Row([dbc.Col(width=1),
    dbc.Col(dbc.Card([
        dbc.CardImg(src='/assets/sensor.png', top=True),]), width=4),
    dbc.Col(dbc.Card([
        dbc.CardImg(src='/assets/diagram.png', top=True),
    ]), width=5),
    ]),
], style={'textAlign':'center'})


@app.callback(
    Output("graph", "figure"), 
    [Input("radio", "value")])
def display_(radio_value):

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['PondLevel'], showlegend=False, name="PondLevel", line_color="red"),
        secondary_y=False,
    )
	
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Rain'], showlegend=False, name="Rain (in.)", line_color="blue"),
        secondary_y=True,
    )
	# can add ,fill='tozeroy' to end of this bracket to fill area under line

	# Add figure title
    #fig.update_layout(
    #    title_text="Farm Pond"
    #)

	# Set x-axis title
    fig.update_xaxes(title_text="Date")

	# Set y-axes titles
    fig.update_yaxes(title_text="<b>Pond Level</b>", color="red", secondary_y=False)
    fig.update_yaxes(title_text="<b>Rain</b>", color="blue", secondary_y=True)

    #manually setting y-axis range for PondLevel
    fig.update_yaxes(range=[-0,4], secondary_y=False)
    fig.update_yaxes(range=[-0,2], secondary_y=True)
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)

    #set range slider and selector buttons for x-axis
    fig.update_xaxes(
    rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

    #set default graph layout as showing only the past month
    now = datetime.date.today()
    then = now - datetime.timedelta(days=30)
    fig.update_layout(xaxis_range=[then, now])


    #return fig
    fig.write_html("graph.html")



# %% [markdown]
# Serve the app using `run_server`.  Unlike the standard `Dash.run_server` method, the `JupyterDash.run_server` method doesn't block execution of the notebook. It serves the app in a background thread, making it possible to run other notebook calculations while the app is running.
#
# This makes it possible to iterativly update the app without rerunning the potentially expensive data processing steps.

# %%
if __name__ == "__main__":
    app.run_server(debug=True)
    

# %% [markdown]
# By default, `run_server` displays a URL that you can click on to open the app in a browser tab. The `mode` argument to `run_server` can be used to change this behavior.  Setting `mode="inline"` will display the app directly in the notebook output cell.

# %%
#app.run_server(mode="inline")

# %% [markdown]
# When running in JupyterLab, with the `jupyterlab-dash` extension, setting `mode="jupyterlab"` will open the app in a tab in JupyterLab.
#
# ```python
# app.run_server(mode="jupyterlab")
# ```

# %%