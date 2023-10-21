import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, callback, Output, Input
import json

df = pd.read_csv(f'../assets/data/dashboard-data.csv', sep='|', nrows=40000, low_memory=False)
dfRegions = pd.read_csv('../assets/data/regions.csv')
dfDepts = pd.read_csv('../assets/data/departement.csv')
df.code_departement = df.code_departement.astype('int').astype('str').str.pad(2, side='left', fillchar='0')

dfScales = {'region': dfRegions, 'departement': dfDepts}
geojson = {}

with open('../assets/data/metropole-version-simplifiee.geojson') as response:
    geojson['metropole'] = json.load(response)

with open('../assets/data/regions-version-simplifiee.geojson') as response:
    geojson['region'] = json.load(response)

with open('../assets/data/departements-version-simplifiee.geojson') as response:
    geojson['departement'] = json.load(response)

echelle = {
    'Departement': 'departement',
    'Region' : 'region',
}

def inputTolist(value):
    if(type(value) == str):
        return [int(value)]
    else:
        return [int(x) for x in value]
    
def card(title, body=[], id=''):
    return html.Div([
            html.H3(children=title, className='cs-card-title'),
            html.Label(id=id, className='cs-card-body')
        ], className='cs-card'),

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div([
        html.Div([
            html.Label(children='Année'),
            dcc.Dropdown(df['annee'].unique(), '2018', id='years-selection', className='select-field', multi=True),
        ], className='filter-name'),

        html.Div([
            html.Label(children='Echelle'),
            dcc.Dropdown(list(echelle.keys()), 'Departement', id='scale-selection', className='select-field'),
        ], className='filter-name'),
    ], style={'display':'flex', 'gap': '16px', 'justifyContent': 'end'}),

    html.Div([
        html.H3(children=[
            html.Span('Chiffres des ventes '), 
            html.Span(id='filter-dates-name'), 
            html.Span(' par '), 
            html.Span(id='filter-scale-name'), 
        ], id='number-title')
    ]),
    html.Div([
        html.Div([
            html.H3(children='Total de vente', className='cs-card-title'),
            html.Label(id='nb-vente', className='cs-card-body')
        ], className='cs-card'),
        html.Div([
            html.H3(children='Moyenne', className='cs-card-title'),
            html.Label(id='avg-vente', className='cs-card-body')
        ], className='cs-card'),
        html.Div([
            html.H3(children='Médiane', className='cs-card-title'),
            html.Label(id='median-vente', className='cs-card-body')
        ], className='cs-card'),
    ], style={'display': 'flex', 'margin': '32px 0', 'gap': '16px'}),
    html.Div([
        html.H3(children='Evolution des ventes en fonciton du temps', id='time-title')
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='graph-content', style={'height':'400px'}),
        ], className='col-md-8'),
        html.Div([
            dcc.Graph(id='years-graph', style={'height':'400px'}),
        ], className='col-md-4'),
    ], className='row', style={ 'display' : 'flex', }),
    html.Div([
        html.H3(children='Représentation géographique des ventes', id='geo-title')
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='graph-map'),
        ], className='col-md-8'),
        html.Div([
            
        ], id='map-details', className='col-md-4'),
    ], className='row'),
    html.Div([
        html.H3(children='Représentation des ventes par Type de bien', id='type-local-title')
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='graph-bar'),
        ], className='col-md-6'),
        html.Div([
            dcc.Graph(id='pie-chart-local'),
        ], className='col-md-6'),
    ], className='row align-items-center'),
], className='mx-3')


@callback(
    [
        Output('nb-vente', 'children'),
        Output('avg-vente', 'children'),
        Output('median-vente', 'children'),
        Output('filter-dates-name', 'children'),
    ],
    Input('years-selection', 'value')
)
def update_stats(value):
    years =inputTolist(value)
    dff = df[df['annee'].isin(years)]
    value = dff['Valeur fonciere']
    if len(years) > 1:
        dates = f'de {min(years)} à {max(years)}'
    elif len(years) == 1:
        dates = f'en {years[0]}'
    else:
        dates = 'par année'
    return dff.shape[0], round(value.mean(), 2), round(value.median(), 2), dates


@callback(
    Output('graph-content', 'figure'),
    Input('years-selection', 'value')
)
def update_graph(value):
    years = inputTolist(value)
    dff = df[df['annee'].isin(years)]
    fig = px.line(
        dff.groupby(['annee', 'mois'])['Valeur fonciere'].mean().reset_index(),
        x='mois',
        y='Valeur fonciere',
        color='annee',
        # title='Évolution de la moyenne de la valeur foncièce au cours de l\'année'
    )
    fig.update_layout(margin={'r': 0, 't': 24, 'l': 0, 'b': 0})
    fig.update_layout(legend={'orientation': 'h', 'yanchor': 'top', 'y': 1.1, 'xanchor': 'right', 'x': 1 , 'bgcolor': 'rgba(255,0,0,0)'})
    return fig

@callback(
    Output('years-graph', 'figure'),
    Input('years-selection', 'value')
)
def update_years_graph(value):
    years = inputTolist(value)
    # dff = df[df['annee'].isin([2018, 2019, 2020, 2021])]
    dff = df[df['annee'].isin(years)]
    fig = px.bar(
        dff.groupby(['annee'])['Valeur fonciere'].mean().reset_index(),
        x='annee',
        y='Valeur fonciere',
        # title='Évolution de la moyenne de la valeur foncièce au cours de l\'année'
    )
    fig.update_layout(margin={'r': 0, 't': 24, 'l': 0, 'b': 0})
    fig.update_layout(legend={'orientation': 'h', 'yanchor': 'top', 'y': 1.1, 'xanchor': 'right', 'x': 1 , 'bgcolor': 'rgba(255,0,0,0)'})
    return fig


@callback(
    Output('graph-bar', 'figure'),
    Input('years-selection', 'value')
)
def update_bar_graph(value):
    years = inputTolist(value)
    dff = df[df['annee'].isin(years)]
    fig = px.histogram(
        dff.groupby(['Type local', 'annee'])['Valeur fonciere'].mean().reset_index(),
        x='Type local',
        y='Valeur fonciere',
        height=300,
        color='annee',
        barmode='group',
        # title='Title'
    )
    fig.update_layout(margin={'r': 0, 't': 24, 'l': 0, 'b': 0})
    fig.update_layout(legend={'orientation': 'h', 'yanchor': 'top', 'y': 1.1, 'xanchor': 'right', 'x': 1 , 'bgcolor': 'rgba(255,0,0,0)'})
    return fig


@callback(
    [
        Output('graph-map', 'figure'),
        Output('filter-scale-name', 'children'),
    ],
    Input('scale-selection', 'value'),
    Input('years-selection', 'value')
)
def update_map(value, year):
    scale = echelle[value]
    years = inputTolist(year)
    dff = df[df['annee'].isin(years)].groupby(['annee', 'code_'+scale])['Valeur fonciere'].mean().reset_index()
    dff = dfScales[scale].merge(dff, how='left', left_on='code_'+scale, right_on='code_'+scale).fillna(0)
    fig = px.choropleth(dff, geojson=geojson[scale], featureidkey='properties.code', locations='code_'+scale, color='Valeur fonciere',
                        projection="mercator", color_continuous_scale=px.colors.sequential.Blues)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(showlegend=False,
                        margin={"r":0,"t":0,"l":0,"b":0},
                    )
    return fig, scale

@callback(
    Output('map-details', 'children'),
    [
        Input('graph-map', 'clickData'),
        Input('scale-selection', 'value'),
        Input('years-selection', 'value')
    ],
        )
def update_figure(clickData, scale, yValues):
    print(type(clickData), clickData, scale)
    if clickData is not None:
        scale = echelle[scale]
        years = inputTolist(yValues)
        # recuperer le code departement ou le code region
        location = clickData['points'][0]['location']
        dff = df[df['annee'].isin(years)][df['code_departement'] == location]
        print(dff.shape[0])
        print(dff['Valeur fonciere'].mean())
        print(dff.population.iloc[0])
        # print(dff.loc[0, 'metre_carre']())
        
    return "blabla"
@callback(
    Output('pie-chart-local', 'figure'),
    Input('years-selection', 'value')
)
def update_pie_local(value):
    years = inputTolist(value)
    dff = df[df['annee'].isin(years)].groupby(['annee', 'Type local'])['Valeur fonciere'].mean().reset_index()
    fig = px.pie(dff, values='Valeur fonciere', names='Type local', title='Proportion')
    # fig.update_layout(legend={'orientation': 'h', 'yanchor': 'top', 'y': 1.02, 'xanchor': 'right', 'x': 1 , 'bgcolor': 'rgba(255,0,0,0)'})
    fig.update_layout(showlegend=False)
    return fig