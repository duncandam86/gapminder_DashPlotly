import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

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
features = {
    'Life Expectancy':'lifeExp',
    'Child Mortality':'child_mortality',
    'Income': 'income',
    'Population': 'population',
    'CO2 emission': 'co2_emission',
    'Human development index': 'hdi',
    'Number of HIV cases': 'hiv_num',
}

body_1 = dbc.Row ([
    dbc.Col([
            html.P('Select x-axis'),
            dcc.Dropdown(
                options = [
                    {'label': k, 'value': v } for k,v in features.items()
               ],
               id='overview_xaxis',
               value = 'lifeExp'
            ),
            html.Br(),
            html.P('Select y-axis'),
            dcc.Dropdown(
                options = [
                    {'label': k, 'value': v } for k,v in features.items()
                ],
                id='overview_yaxis',
                value = 'income'
            ),
            html.Br(),
            html.P('Choose year(s)'),
            dcc.Dropdown(
                options = [
                    {'label': i, 'value': i } for i in range(1800,2019)
               ],
               id ='overview_year',
               multi = True,
               value = [2005, 2015]
            ),
    ],width = 3),
        
    dbc.Col([
            dbc.Tabs(
                id="tabs", 
                active_tab = 'overview_visual',
                children = [
                    dbc.Tab(label='Data Visualization', tab_id='overview_visual'),
                    dbc.Tab(label='Data Table', tab_id='overview_table')
                ]
            ),
            html.Div(id='tab-content')
    ],width = 9)    
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

#call back for Tabs in Overview page
@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'active_tab')],
)

def render_content(tab):
    if tab == 'overview_visual':
        return html.Div([
            html.P('there will be a few graphs')
        ])
    elif tab == 'overview_table':
        return html.Div([
            html.P('there will be datatable')
        ])

#run app
if __name__ == '__main__':
    app.run_server(port=8000)

