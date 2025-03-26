from dash import Dash, html, dcc, callback, Output, Input, dcc
import plotly.express as px
from plotly.graph_objs import *
import pandas as pd

countries_df = pd.read_csv('data/countries.csv')            #loading all dataframes and formatting

results_df = pd.read_csv('data/world_cup_finals_data.csv')

countries_arr = countries_df['name'].values

wins_count = results_df['Winner'].value_counts().reset_index()
wins_count.columns = ['Winners', 'Num of World Cups Won']


all_countries_fig = px.choropleth(wins_count, 
        scope="world",
        locationmode='country names',
        locations='Winners',
        color='Num of World Cups Won',              #setting up initial maps
        color_continuous_scale='Bluered_r'
    ) 

all_countries_fig.update_layout(
        title_text=f"World Map of all World Cup Winners",
        title_x=0.5,
    )

empty_fig = px.choropleth(pd.DataFrame([]))

app = Dash(__name__)

app.layout = html.Div([
    html.H1('World Cup Finals Data', style={'text-align':'center'}),
    dcc.RadioItems(
        id='radio-selection',
        options=[
            {'label': 'a. All World Cup Winners', 'value': 'All'},
            {'label': 'b. Search World Cup Victories by Country', 'value': 'Specific Country'},
            {'label': 'c. Search World Cup Result by Year', 'value': 'World Cup Year'},
        ],
        value='All'
    ),
    html.Div([
        dcc.Graph(id='graph1', figure=all_countries_fig),
    ], id='all-countries-div'),

    html.Div([
        html.H4('Select a Country:'),
        dcc.Dropdown(id='country-dropdown', options=countries_arr,
        value='Brazil',
        ), dcc.Graph(id='graph2', figure=empty_fig),
    ], id='country-div'
    ),
    html.Div([
        html.H4('Select Year:'),
        dcc.Dropdown(id='year-dropdown', options=[
            {'label': '1930', 'value': '1930'},
            {'label': '1934', 'value': '1934'},
            {'label': '1938', 'value': '1938'},
            {'label': '1950', 'value': '1950'},
            {'label': '1954', 'value': '1954'},
            {'label': '1958', 'value': '1958'},
            {'label': '1962', 'value': '1962'},
            {'label': '1966', 'value': '1966'},
            {'label': '1970', 'value': '1970'},
            {'label': '1974', 'value': '1974'},
            {'label': '1978', 'value': '1978'},
            {'label': '1982', 'value': '1982'},
            {'label': '1986', 'value': '1986'},
            {'label': '1990', 'value': '1990'},
            {'label': '1994', 'value': '1994'},
            {'label': '1998', 'value': '1998'},
            {'label': '2002', 'value': '2002'},
            {'label': '2006', 'value': '2006'},
            {'label': '2010', 'value': '2010'},
            {'label': '2014', 'value': '2014'},
            {'label': '2018', 'value': '2018'},
            {'label': '2022', 'value': '2022'},
        ],
        value='2022',
        ),
        dcc.Graph(id='graph3', figure=empty_fig),
    ], id='year-div'
    ),
], style={'background-color': 'white', 'color': 'black', 'font-family':'verdana'})

@app.callback(
    Output('all-countries-div', 'style'),
    Output('country-div', 'style'),
    Output('year-div', 'style'),
    Input('radio-selection', 'value'),
)

def hiding_inputs(value):
    if value == "All":
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    
    elif value == "Specific Country":
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    
    elif value == "World Cup Year":
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

@app.callback(
    Output("graph2", "figure"),
    Input("country-dropdown", "value"),
    )

def display_country(country):
    country_data = countries_df[countries_df['name'] == country].copy()

    if wins_count['Winners'].str.contains(country, na=False).any():
        amount_won = wins_count.loc[wins_count['Winners'] == country, 'Num of World Cups Won']
        amount_won = amount_won.iloc[0]
    else:
        amount_won = 0
        
    country_data['Num of World Cups Won'] = amount_won
        
    lat, long = country_data.iloc[0]['latitude'], country_data.iloc[0]['longitude']
        

    fig = px.choropleth(country_data, 
        scope="world",
        locationmode='country names',
        locations='name',
        hover_data='Num of World Cups Won',
    ) 
        
    fig.update_layout(
        geo=dict(
        projection_scale=3,
            center={"lat": lat, "lon": long},  
        ),
        title_text=f"<b>{country}</b> has won <b>{amount_won}</b> World Cups.",
        title_x=0.5,
    )

    return fig

@app.callback(
    Output("graph3", "figure"),
    Input("year-dropdown", "value"),
    )

def display_year(year):
    world_cup_result_df = results_df[results_df['Year'] == int(year)].copy()
    world_cup_result_df.drop(columns=['Year'], inplace=True)
    world_cup_result_df = world_cup_result_df.T
    world_cup_result_df = world_cup_result_df.rename(columns={world_cup_result_df.columns[0]: "Country"})

    winner = world_cup_result_df['Country'].iloc[0]
    runner_up = world_cup_result_df['Country'].iloc[1]
        
    fig = px.choropleth(world_cup_result_df, 
        scope="world",
        locationmode='country names',
        locations='Country',
        color=world_cup_result_df.index,
    ) 

    fig.update_layout(
        title_text=f"In {year}, <b>{winner}</b> won the World Cup against <b>{runner_up}</b>.",
        title_x=0.5,
    )
    return fig

app.run(debug=True)