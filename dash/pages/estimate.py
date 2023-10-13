import dash
from dash import Dash, dcc, html, Input, Output, callback

fields = [
    {'name': 'surface', 'placeholder' : 'Surface', 'type': 'text'},
    {'name': 'Type', 'placeholder' : 'Type', 'type': 'text'}
]

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

dash.register_page(__name__)
layout = html.Div('Fomulaire ici')

# @callback(
#     Output("out-all-types", "children"),
#     [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
# )
# def cb_render(*vals):
#     print(vals)
#     return " | ".join((str(val) for val in vals if val))
