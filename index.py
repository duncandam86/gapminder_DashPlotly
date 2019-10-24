import pandas as pd
import numpy as np
import dash
import dash_table as dt
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.config.suppress_callback_exceptions = True

#import data
df = pd.read_csv('Data/gapminder_dd.csv')

df.columns = ['Country', 'Year', 'Life Expectancy', 'Child Mortality (per 1000 born)', 'Income (per person)', 'Population', 
            'CO2 emission (tonnes per person)', 'Human Development Index', 'Number of HIV cases', 'Continent']


#navbar 
navbar = dbc.NavbarSimple(
            children=[
                dbc.NavLink("Overview", href="/", id="page-1-link"),
                dbc.NavLink("Continent", href="/continent", id="page-2-link"),
                dbc.NavLink("Country", href="/country", id="page-3-link"),
            ],
            brand="Gapminder",
            brand_href="/",
            color="primary",
            dark=True
)

#body content for overview
df_1 = df.drop(columns = ['Year', 'Country', 'Continent'])

body_1 = dbc.Row ([
    dbc.Col([
            html.P('Select x-axis:'),
            dcc.Dropdown(
                options = [
                    {'label': i, 'value': i } for i in df_1.columns
               ],
               id='overview_xaxis',
               value = 'Life Expectancy'
            ),
            html.Br(),
            html.P('Select y-axis:'),
            dcc.Dropdown(
                options = [
                    {'label': i, 'value': i } for i in df_1.columns
                ],
                id='overview_yaxis',
                value = 'Income (per person)'
            ),
            html.Br(),
            html.P('Choose year:'),
            dcc.Dropdown(
                options = [
                    {'label': i, 'value': i } for i in range(1800,2019)
               ],
               id ='overview_year',
               value = 2005
            ),
    ],width = 3),
        
    dbc.Col([
            dbc.Tabs(
                id="tabs", 
                active_tab = 'overview_visual',
                children = [
                    dbc.Tab(
                        label='Data Visualization', 
                        tab_id='overview_visual',
                        children = [
                            dcc.Graph(
                                    id = 'overview_graph'
                                ),    
                            html.Hr(style = {'width' : '95%'}),
                            dcc.Graph(
                                    id = 'xaxis_graph'
                            ),                                
                            html.Hr(style = {'width' : '95%'}),
                            dcc.Graph(
                                    id = 'yaxis_graph'
                            )
                        ]
                    ), 
                    dbc.Tab(
                        label='Data Table', 
                        tab_id='overview_table',
                        children = dt.DataTable(
                            id = 'table_1',
                            sort_action="native",
                            style_cell={'textAlign': 'left', 'fontFamily' : 'Courier', 'fontSize':'11pt','textOverflow':'clip'},
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'lightgray',
                                'fontWeight': 'bold'
                            },
                            style_table = {'overflowY':'scroll'},
                            style_data_conditional=[
                                {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ],
                            fixed_rows={ 'headers': True, 'data': 0 },
                            style_cell_conditional=[
                                {'if': {'column_id': 'Country'},
                                'width': '20%'},
                                {'if': {'column_id': 'Continent'},
                                'width': '20%'},
                                {'if': {'column_id': 'Income (per person)'},
                                'width': '30%'},
                                {'if': {'column_id': 'CO2 emission (tonnes per person)'},
                                'width': '30%'},
                                {'if': {'column_id': 'Human Development Index'},
                                'width': '30%'},
                                {'if': {'column_id': 'Child Mortality (per 1000 born)'},
                                'width': '30%'},
                                {'if': {'column_id': 'Population'},
                                'width': '30%'},
                                {'if': {'column_id': 'Number of HIV cases'},
                                'width': '30%'}
                            ]
                        )
                    )
                ]
            )
    ],width = 9)    
])

#body content for continent
body_2 = dbc.Row ([
    dbc.Col([
        html.P('Select x-axis:'),
        dcc.Dropdown(
                options = [
                    {'label': i, 'value': i } for i in df_1.columns
               ],
               id='cont_xaxis',
               value = 'Life Expectancy'
            ),
            html.Br(),
            html.P('Select y-axis:'),
            dcc.Dropdown(
                options = [
                    {'label': i, 'value': i } for i in df_1.columns
                ],
                id='cont_yaxis',
                value = 'Income (per person)'
            ),
            html.Br(),
            html.P('Select a continent:'),
            dcc.RadioItems(
                id = 'cont',
                options=[
                    {'label': ' {}'.format(cont), 'value': cont} for cont in df['Continent'].unique()
                ],
                value='Asia',
                labelStyle = {'display':'block'}
            ),
            html.Br(),
            html.P('Choose year:'),
            dcc.Dropdown(
                options = [
                    {'label': i, 'value': i } for i in range(1800,2019)
                ],
                id ='cont_year',
                value = 2005
            ),      
        ],width = 3),
    dbc.Col([
        dbc.Tabs(
            id="tabs", 
            active_tab = 'cont_visual',
            children = [
                dbc.Tab(
                    label='Data Visualization', 
                    tab_id='cont_visual',
                    children = [
                        dbc.Col([
                            dcc.Graph(
                                id = 'cont_graph'
                            ),    
                        ], width = 12),
                        html.Hr(style = {'width' : '95%'}),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(
                                    id = 'cont_pie_xaxis'
                                ),    
                            ], width = 6),
                            dbc.Col([
                                dcc.Graph(
                                    id = 'cont_pie_yaxis'
                                ),    
                            ], width = 6),
                        ])
                    ]             
                ), 
                dbc.Tab(
                    label='Data Table', 
                    tab_id='cont_table',
                    children = dt.DataTable(
                        id = 'table_2',
                        sort_action="native",
                        style_cell={'textAlign': 'left', 'fontFamily' : 'Courier', 'fontSize':'11pt','textOverflow':'clip'},
                        style_as_list_view=True,
                        style_header={
                            'backgroundColor': 'lightgray',
                            'fontWeight': 'bold'
                        },
                        style_table = {'overflowY':'scroll'},
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ],
                        fixed_rows={ 'headers': True, 'data': 0 },
                        style_cell_conditional=[
                            {'if': {'column_id': 'Country'},
                            'width': '20%'},
                            {'if': {'column_id': 'Year'},
                            'width': '20%'},
                            {'if': {'column_id': 'Income (per person)'},
                            'width': '30%'},
                            {'if': {'column_id': 'CO2 emission (tonnes per person)'},
                            'width': '30%'},
                            {'if': {'column_id': 'Human Development Index'},
                            'width': '30%'},
                            {'if': {'column_id': 'Child Mortality (per 1000 born)'},
                            'width': '30%'},
                            {'if': {'column_id': 'Population'},
                            'width': '30%'},
                            {'if': {'column_id': 'Number of HIV cases'},
                            'width': '30%'}
                        ]
                    )
                )
            ]
        )      
    ],width = 9)
])

#body content for country
body_3 = [dbc.Row ([
    dbc.Col([
        html.P('Select a catergory:'),
        dcc.RadioItems(
            id = 'country_cat',
            options = [{'label': ' {}'.format(cat), 'value': cat} for cat in df_1.columns],
            labelStyle = {'display':'block'}, 
            value = 'Income (per person)'
        ),
        html.Br(),
        html.P('Select country:'),
        dcc.Dropdown(
            id = 'country',
            options = [{'label': country, 'value': country} for country in df['Country'].sort_values().unique()],
            multi = True,
            value = ['Vietnam','Gabon','Tuvalu','Slovenia','Jamaica','Chile']
        ),    
    ],width = 3),
    dbc.Col([
        dbc.Tabs([
            dbc.Tab( 
                label = 'Data Visualization',
                children = [
                    dbc.Col([
                        dcc.Graph(
                            id = 'country_compare_cat'
                        )
                    ],width = 12),
                ]      
            ),
            dbc.Tab(
                label='Data Table', 
                children = dt.DataTable(
                    id = 'table_3',
                    sort_action="native",
                    style_cell={'textAlign': 'left', 'fontFamily' : 'Courier', 'fontSize':'11pt','textOverflow':'clip'},
                    style_as_list_view=True,
                    style_table = {'overflowY':'scroll'},
                    style_header={
                        'backgroundColor': 'lightgray',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    fixed_rows={ 'headers': True, 'data': 0 },
                    style_cell_conditional=[
                        {'if': {'column_id': 'Country'},
                        'width': '20%'},
                        {'if': {'column_id': 'Year'},
                        'width': '20%'},
                         {'if': {'column_id': 'Continent'},
                        'width': '20%'},
                        {'if': {'column_id': 'Income (per person)'},
                        'width': '30%'},
                        {'if': {'column_id': 'CO2 emission (tonnes per person)'},
                        'width': '30%'},
                        {'if': {'column_id': 'Human Development Index'},
                        'width': '30%'},
                        {'if': {'column_id': 'Child Mortality (per 1000 born)'},
                        'width': '30%'},
                        {'if': {'column_id': 'Population'},
                        'width': '30%'},
                        {'if': {'column_id': 'Number of HIV cases'},
                        'width': '30%'}
                    ]
                )
            )
        ])       
    ],width = 9),
]), 
html.Hr(style = {'width':'95%'}), 
html.P(
    id = 'selected_years'
),
dcc.RangeSlider(
    id = 'country_year',
    marks = {year : '{}'.format(year) for year in range (1801,2019,10)},
    min = 1801,
    max = 2018,
    step = 1,
    value = [1995,2005]
),
html.Br(),
dbc.Row([
    dbc.Col([
        dcc.Graph(
            id = 'graph_large'
        )
    ], width = 12)
])]

#Layout set up
app.layout = html.Div([dcc.Location(id='url'),navbar, dbc.Container(id="page-content", className="pt-4")])

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

#=======Rendering Overview Tab=========================================
#call back for overview_graph
continents = df['Continent'].unique()
colors = ['salmon','green','orange','indigo','blue','red']
con_col = dict(zip(continents, colors))

@app.callback(
    Output('overview_graph','figure'),
    [Input('overview_xaxis','value'),
    Input('overview_yaxis','value'),
    Input('overview_year','value')]
)
#function to render overview graph
def render_overview_graph(xaxis, yaxis, year):
    traces = []
    for cont,col in con_col.items():
        df_year = df[df['Year'] == year]
        df_year_cont = df_year[df_year['Continent'] == cont]
        hover_text = []
        for i, row in df_year_cont.iterrows():
            hover_text.append(('Country: {country}<br>'+
                            '{xaxis}: {rowxaxis} <br>'+
                            '{yaxis}: {rowyaxis} <br>'+
                                'Year: {year}').format(country=row['Country'],
                                                    xaxis= xaxis,
                                                    rowxaxis = row[xaxis],
                                                    yaxis= yaxis,
                                                    rowyaxis = row[yaxis],
                                                    year=row['Year']))
        trace = go.Scatter(
            x = df_year_cont[xaxis],
            y = df_year_cont[yaxis],
            mode = 'markers',
            marker = dict(symbol = 0, 
                    color = col, 
                    size  = df_year_cont['Population'],
                    sizemode = 'area',
                    sizeref  = 2*max(df_year['Population'])/(60.**2),
                    sizemin = 5,
                    opacity = 0.7),
            name = cont,
            hovertext = hover_text
        )
        traces.append(trace)
    
    layout = go.Layout(
        xaxis = dict(title = xaxis,showgrid = True, gridcolor = 'lightgray'),
        yaxis = dict(title = yaxis,showgrid = True, gridcolor = 'lightgray'),
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
    )
        
    fig = go.Figure(data = traces, layout = layout)
    
    fig.update_layout(
        height =  400,
        margin = dict(t = 30)
    )
    return fig

#call back for xaxis_graph vs year
@app.callback(
    Output('xaxis_graph', 'figure'),
    [Input('overview_xaxis','value')]
)
def render_xaxis_graph(xaxis):
    df_cont_year = df.groupby(['Continent','Year'])[xaxis].mean().reset_index()
    traces = []
    for cont,col in con_col.items():
        trace = go.Scatter(
            x = df_cont_year['Year'],
            y = df_cont_year[df_cont_year['Continent']==cont][xaxis],
            mode = 'markers+lines',
            name = cont,
            marker = dict(color = col),
            line = dict(color = col),
        )
        traces.append(trace)

    layout = go.Layout(
        title = '{} over year'.format(xaxis),
        yaxis = dict(title = xaxis,showgrid = True, gridcolor = 'lightgray'),
        xaxis = dict(showgrid = True, gridcolor = 'lightgray'),
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
    )
    
    fig = go.Figure(data = traces, layout = layout)
    
    fig.update_layout(
        height =  400,
        margin = dict(t = 30)
        
    )
    return fig

#call back for yaxis_graph vs year
@app.callback(
    Output('yaxis_graph', 'figure'),
    [Input('overview_yaxis','value')]
)
def render_yaxis_graph(yaxis):
    df_cont_year = df.groupby(['Continent','Year'])[yaxis].mean().reset_index()
    traces = []
    for cont,col in con_col.items():
        trace = go.Scatter(
            x = df_cont_year['Year'],
            y = df_cont_year[df_cont_year['Continent']==cont][yaxis],
            mode = 'markers+lines',
            name = cont,
            marker = dict(color = col),
            line = dict(color = col),
        )
        traces.append(trace)

    layout = go.Layout(
        title =  '{} over year'.format(yaxis), 
        yaxis = dict(title = yaxis,showgrid = True, gridcolor = 'lightgray'),
        xaxis = dict(showgrid = True, gridcolor = 'lightgray'),
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
    )
    
    fig = go.Figure(data = traces, layout = layout)
    
    fig.update_layout(
        height =  400,
        margin = dict(t = 30)
    )
    return fig

#call back for data class of datatable
@app.callback(
    Output('table_1','data'),
    [Input('overview_year','value'),
    Input('overview_xaxis','value'),
    Input('overview_yaxis','value'),
    Input('table_1', 'page_current'),
    Input('table_1', 'page_size')]
)
def render_data_overview_table(year,xaxis, yaxis, page_current, page_size):
    df_year = df[df['Year']==year][['Country',xaxis, yaxis,'Continent']]
    # df_year = df_year.iloc[page_current*page_size:(page_current+ 1)*page_size]
    data = df_year.to_dict('records')    
    return data

#call back for column class of datatable
@app.callback(
    Output('table_1','columns'),
    [Input('overview_year','value'),
    Input('overview_xaxis','value'),
    Input('overview_yaxis','value')]
)
def render_columns_overview_table(year,xaxis, yaxis):
    df_year = df[df['Year']==year][['Country',xaxis, yaxis,'Continent']]
    columns = [{'id': c, 'name': c} for c in df_year.columns]  
    return columns

#+++++++---------------+++++++Rendering continent tab-----------------
#call back for cont_graph 
@app.callback(
    Output('cont_graph','figure'),
    [Input('cont_xaxis','value'),
    Input('cont_yaxis','value'),
    Input('cont','value'),
    Input('cont_year','value')]
)

def render_cont_graph(xaxis,yaxis,cont,year):
    df_cont_year = df[(df['Continent'] == cont) & (df['Year'] == year)]
    hover_text = []
    for i, row in df_cont_year.iterrows():
        hover_text.append(('Country: {country} <br>'+
                        '{xaxis}: {rowxaxis} <br>'+
                        '{yaxis}: {rowyaxis} <br>').format(
                            country = row['Country'],
                            xaxis =  xaxis,
                            rowxaxis = row[xaxis],
                            yaxis = yaxis,
                            rowyaxis = row[yaxis]))
    
    data = [go.Scatter(
        x = df_cont_year[xaxis],
        y = df_cont_year[yaxis],
        mode = 'markers',
        marker = dict(symbol = 0, 
                    color = 'blue', 
                    size  = df_cont_year['Population'],
                    sizemode = 'area',
                    sizeref  = 2*max(df_cont_year['Population'])/(40.**2),
                    sizemin  = 6),
        hovertext = hover_text
    )]

    layout = go.Layout(
        xaxis = dict(title = xaxis, showgrid = True, gridcolor = 'lightgray'),
        yaxis = dict(title = yaxis, showgrid = True, gridcolor = 'lightgray'),
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
        margin = dict(t = 30) 
    )

    figure = go.Figure(data = data, layout = layout)
    return figure

#call back for cont_pie_xaxis
@app.callback(
    Output('cont_pie_xaxis','figure'),
    [Input('cont_xaxis','value'),
    Input('cont','value'),
    Input('cont_year','value')]
)

def render_cont_pie_xaxis(xaxis, cont, year):
    df_cont_year = df[(df['Continent']==cont) & (df['Year']==year)]
    data = [go.Pie(
        labels = df_cont_year['Country'],
        values = df_cont_year[xaxis],
        showlegend = False,
        textinfo = 'label+value',
        hoverinfo = 'label+percent+value',
        textposition = 'inside',
        hole = 0.6,
        opacity = 0.85
    )] 
    layout = go.Layout(
        title = dict(text = '{} of {} in {}'.format(xaxis,cont,year),pad = dict(l=30)),
        # width = 320,
        margin = dict(l=10, r=10, t=30,b=10)
    )
    figure =  go.Figure(data = data, layout = layout)
    return figure

#call back for cont_pie_yaxis
@app.callback(
    Output('cont_pie_yaxis','figure'),
    [Input('cont_yaxis','value'),
    Input('cont','value'),
    Input('cont_year','value')]
)

def render_cont_pie_yaxis(yaxis, cont, year):
    df_cont_year = df[(df['Continent']==cont) & (df['Year']==year)]
    data = [go.Pie(
        labels = df_cont_year['Country'],
        values = df_cont_year[yaxis],
        showlegend = False,
        textinfo = 'label+value',
        hoverinfo = 'label+percent+value',
        textposition = 'inside',
        hole = .6,
        opacity = 0.85
    )] 
    layout = go.Layout(
        title = dict(text = '{} of {} in {}'.format(yaxis,cont,year), pad = dict(l=30)),
        # width = 320,
        margin = dict(l=10, r=10, t=30,b=10)
    )
    figure =  go.Figure(data = data, layout = layout)
    return figure

#call back for cont table data class
@app.callback(
    Output('table_2','data'),
    [Input('cont_xaxis','value'),
    Input('cont_yaxis','value'),
    Input('cont','value'),
    Input('cont_year','value')]
)

def render_cont_table_data(xaxis, yaxis, cont, year):
    df_cont_year = df[(df['Continent']==cont) & (df['Year'] == year)]
    df_cont_year = df_cont_year[['Country','Year',xaxis,yaxis]]
    data = df_cont_year.to_dict('records')
    return data

#call back for cont table columns class
@app.callback(
    Output('table_2','columns'),
    [Input('cont_xaxis','value'),
    Input('cont_yaxis','value'),
    Input('cont','value'),
    Input('cont_year','value')]
)

def render_cont_table_columns(xaxis, yaxis, cont, year):
    df_cont_year = df[(df['Continent']==cont) & (df['Year'] == year)]
    df_cont_year_column = df_cont_year[['Country','Year',xaxis,yaxis]]
    columns = [{'id' : col, 'name':col} for col in df_cont_year_column.columns]
    return columns

#==================== Render country tab ============================
# df_country = df[df['Country']=='Vietnam']['Population'].values
# print(df_country)

#call back to country_graph_cat
@app.callback(
    Output('country_compare_cat', 'figure'),
    [Input('country','value'),
    Input('country_cat','value')]
)
#rendering country_graph_cat1
def render_country_compare_cat(country,cat):
    data = []
    for c in country:
        df_country = df[df['Country'] == c]
        hover_text = []
        for i, row in df_country.iterrows():
            hover_text.append(('Country: {country} <br>'+
                                '{cat} : {rowcat} <br>' +
                                'Year: {year}').format(country=row['Country'],
                                                    cat = cat,
                                                    rowcat = row[cat],
                                                    year=row['Year']))
        trace = go.Scatter(
            x = df_country['Year'],
            y = df_country[cat],
            mode = 'markers+lines',
            marker = dict(size = 6),
            name = c,
            hovertext = hover_text,
            fill ='tozeroy',
            fillcolor= 'rgba(169, 169, 169,0.1)'
        )
        data.append(trace) 

    layout = go.Layout(
        title = dict(text = '{cat} over year'.format(cat = cat), pad = dict(l = 0)),
        xaxis = dict(showgrid = True, gridcolor = 'lightgray'),
        yaxis = dict(title = cat, showgrid = True, gridcolor = 'lightgray'),
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
        margin = dict(t=60, b = 30),
        height =  400,
        barmode = 'group'
    )

    figure = go.Figure(data = data, layout = layout)

    return figure

#call back for country datatable data
@app.callback(
    Output('table_3','data'),
    [Input('country','value'),
    Input('country_cat', 'value')]
)

#rendering data class of country datatable 
def rendering_country_table_data(country, cat):
    df_country = df[df['Country'].isin(country)][['Country','Year',cat,'Continent']]
    data = df_country.to_dict('records')
    return data

#call back for country datatable columns
@app.callback(
    Output('table_3','columns'),
    [Input('country','value'),
    Input('country_cat','value')]
)

#rendering columns class of country datatable
def rendering_country_table_column(country, cat):
    df_country = df[df['Country'].isin(country)][['Country','Year',cat,'Continent']]
    columns = [{'id':col, 'name': col} for col in df_country.columns]
    return columns

#call back selected range   
@app.callback(
    Output('selected_years','children'),
    [Input('country_year', 'value')]
)
#rendering selected range
def render_range_year(value):
    text = html.B('Selected range: {} to {}'.format(value[0],value[1]), 
                        style = {'color':'gray'})
    return text 

#call back large graph (box plot)
@app.callback(
    Output('graph_large','figure'),
    [Input('country_year','value'),
    Input('country','value'),
    Input('country_cat','value')]
)
#rendering large graph (box plot)
def render_large_graph(years, countries, cat):
    data = []
    year_range = list(range(years[0], years[1]+1))
    for c in countries:
        df_country = df[df['Country'] == c]
        df_country_year = df_country[df_country['Year'].isin(year_range)]
        trace = go.Violin(
            y = df_country_year[cat],
            x = df_country_year['Country'],
            name = c,
            box_visible = True,
            meanline_visible=True,
            jitter = 0.3
        )
        data.append(trace)
    
    layout = go.Layout(
        title = dict(text = 'Comparison of {cat} from {year1} to {year2}'.format(cat = cat, year1 = years[0], year2=years[1])),
        yaxis = dict(title = cat, showgrid = True, gridcolor = 'lightgray'),
        xaxis = dict(showgrid = True, gridcolor = 'lightgray'),
        margin = dict (t = 80),
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',
        showlegend = False
    )

    figure = go.Figure (data = data, layout = layout) 
    return figure


#run app
if __name__ == '__main__':
    app.run_server(port = 8000, debug = True)

