import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


#import data
df = pd.read_csv('Data/gapminder_dd.csv')
print(df.head())


#navbar 
navbar = dbc.NavbarSimple(
        children=[
            dbc.NavLink("Overview", href="/", id="page-1-link"),
            dbc.NavLink("Continent", href="/continent", id="page-2-link"),
            dbc.NavLink("Country", href="/country", id="page-3-link"),
        ],
        brand="Gapminder",
        brand_href="#",
        color="primary",
        dark=True
    )

#body content for overview
body_1 = dbc.Row ([
    dbc.Col([
            html.H1('Selection goes here')
        ],width = 4),
        dbc.Col([
            html.H2('Graph goes here')
        ],width = 8)    
])

#body content for continent

body_2 = dbc.Row ([
    dbc.Col([
            html.H1('Selection goes here for continent')
        ],width = 4),
        dbc.Col([
            html.H2('Graph goes here for contient')
        ],width = 8)
])

#body content for country
body_3 = dbc.Row ([
    dbc.Col([
            html.H1('Selection goes here for country')
        ],width = 4),
        dbc.Col([
            html.H2('Graph goes here for country')
        ],width = 8)
])

#Layout set up
app.layout = html.Div([dcc.Location(id='url'),navbar, dbc.Container(id="page-content", className="pt-4"),])


#Server setup



#call back to activate toggle between pages/tabs
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]

#callback to swtich content of the page when click on link on navbar
@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname in ["/", "/overview"]:
        return body_1
    elif pathname == "/continent":
        return body_2
    elif pathname == "/country":
        return body_3
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



#run app
if __name__ == '__main__':
    app.run_server(port=8000)

