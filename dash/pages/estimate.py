import dash
import requests
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback, State

fields = [
    {'type': 'number', 'label' : 'Nombre de lot', 'id': 'nb-lots'},
    {'type': 'number', 'label' : 'Nombre de pièces principales', 'id': 'nb-pieces'}
]
fields = [
    {'id': 'select-departement'},
    {'id': 'select-type-local'},
    {'id': 'surfaces'},
    {'id': 'nb-pieces'},
]

dash.register_page(__name__)
# form = dbc.Row(
#     [
#         dbc.Col(
#             dbc.FormFloating([
#                 dbc.Input(type=f['type'], id=f['id'], placeholder=f['label']),
#                 dbc.Label(f['label']),
#             ]),
#             width=6,
#         ) for f in fields
#     ],
#     className='mb-3',
# )

layout = html.Div([
    html.H3('Localisation', className='mb-3'),
    dbc.Row([
        dbc.Col(
            dbc.FormFloating([
                dbc.Select(
                    id="select-region",
                    options=[
                        {"label": "Option 0", "value": "0"},
                        {"label": "Option 1", "value": "1"},
                        {"label": "Option 2", "value": "2"},
                    ],
                    value='0'
                ),
                dbc.Label(['Région']),
            ]),
            width=6
        ),
        dbc.Col(
            dbc.FormFloating([
                dbc.Select(
                    id="select-departement",
                    options=[{"label": "Option 0", "value": "0"},],
                    value='0'
                ),
                dbc.Label(['Département']),
            ]),
            width=6
        ),
    ], className='mb-5'),
    html.H3('Caractéristiques du bien', className='mb-3'),
    dbc.Row([
        dbc.Col(
            dbc.FormFloating([
                dbc.Select(
                    id="select-type-local",
                    options=[
                        {"label": "Option 0", "value": '12', 'selected': True},
                        {"label": "Option 1", "value": "1"},
                        {"label": "Option 2", "value": "2"},
                    ],
                    value='12',
                ),
                dbc.Label(['Type']),
            ]),
            width=4
        ),
        dbc.Col(
            dbc.FormFloating([
                dbc.Input(type='number', id='surfaces', placeholder='surface'),
                dbc.Label('Surface'),
            ]),
            width=4
        ),
        dbc.Col(
            dbc.FormFloating([
                dbc.Input(type='number', id='nb-pieces', placeholder='surface'),
                dbc.Label('Nombre de pièces principales'),
            ]),
            width=4
        ),
    ], className='mb-4'),
    dbc.Button('Estimer', color='primary', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic')
], className='container')

@callback(
    Output('select-departement', 'options'),
    Input('select-region', 'value')
)
def update_depts(value):
    if(not value):
        return []
    return [
        {"label": "Option 0", "value": "1", "selected": 'selected'},
        {"label": "Option 1", "value": "1"},
        {"label": "Option 2", "value": "2"},
        {"label": "Disabled option", "value": "3", "disabled": True}
    ]

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    [State(f['id'], 'value') for f in fields],
    prevent_initial_call=True
)
def update_output(n_clicks, value, value2):
    response = requests.get(f'http://127.0.0.1:5000/estimate?nb-lot={value}&nb-piece={value2}')
    response = response.json()['data']
    return f'Selon les informations fournies votre propriété est estimée à : {response}'
