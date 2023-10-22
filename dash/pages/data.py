import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback, State, dash_table

df = pd.read_csv(f'../assets/data/new-dashboard-data.csv', sep='|', nrows=40000, low_memory=False)
df = df[['Date mutation', 'Nature mutation', 'Type local', 'Surface', 'Nombre pieces principales', 'Valeur fonciere', 'nom_region', 'departement', 'Commune', 'population']]



dash.register_page(__name__)

layout = html.Div([
    html.Div([
        html.H3('La liste des ventes de biens immobiliers'),
        html.Button('Ajouter des données', className='btn btn-primary'),
    ], className='d-flex justify-content-between align-items-center mb-3'),
    dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        data=df.to_dict('records'), 
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=25
    ),
], className='container', style={'overflow': 'scroll auto'})