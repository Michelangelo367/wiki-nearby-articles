from logging import PlaceHolder
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import math
import numpy as np
import requests 
import re
from wikinearbyarticles.bin.helpers import helpers

# TODO add animations 
# TODO between graphs as they are updated, extending graphs


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, 
        # external_stylesheets=[dbc.themes.DARKLY]
        external_stylesheets=external_stylesheets
        )

app.layout = html.Div([
    
    html.Div(
        html.P(
            "wiki nearby articles",
            style = {
                "font-size": "72px",
                "fontFamily": "monospace",
                "letter-spacing": "5px",
                "text-align": "center",
                "font-weight": "light",
                "color": "#525252"
            }
        )
    ),
    html.Div(
        html.Hr(),
        style = {
            "padding-bottom": "1px"
        }
    ),
    # html.Div(
    #     html.Hr()
    # ),
    html.Div(
        html.P("enter article link below"),
        style={
                "font-size": "13px",
                "letter-spacing": "2px",
                "fontFamily": "monospace",
                "margin": "0  auto",
                "display": "center",
                'width': '100%',
                'text-align': 'center',
                # 'padding-left':'10%', 'padding-right':'10%',
                "border": "none",
                "border-bottom": "2px solid #5c5c5c",
                # "background-color": "#1a1a1a",
                "color": "#9c9c9c",
                "padding-bottom": "3px"
                }
    ),

    html.Div([
        dcc.Input(id = "art_link", 
        className = "text_input",
        # placeholder = "enter wikipedia article link",
        value = "https://en.wikipedia.org/wiki/MissingNo.",
        style={
                "font-size": "18px",
                "fontFamily": "monospace",
                "margin": "0  auto",
                "display": "center",
                'width': '100%',
                'text-align': 'center',
                "text-spacing": "1px",
                # 'padding-left':'10%', 'padding-right':'10%',
                "border": "none",
                "border-bottom": "2px solid #5c5c5c",
                # "background-color": "#1a1a1a",
                "color": "#525252",
                "padding-bottom": "3px"
                }),

    ]),
    html.Div([
        html.Div(
            dcc.Dropdown(
            id = "choose-section-forward",
            # ! options will depend upon the link
            # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = forward_points, points_in_one_plot= 15))]
        )),
        html.Div(dcc.Dropdown(
            id = "choose-section-backward",
            # ! options will depend upon the link
            # options = [{"label": f"section number: {i}", "value": f"{section}"} for i,section in enumerate(get_points(points = backward_points, points_in_one_plot= 15))]
        ))
        
    ]),
    html.Div([
        html.Div(
            html.P("article directs to these articles"),
            style = {
                "width": "48%",
                "font-size": "18px",
                "letter-spacing": "5px",
                "font-family": "monospace",
                "display": "inline-block",
                "text-align": "center"
            }
        ),
        html.Div(
            html.P(),
            style = {
                "width": "2%",
                "display": "inline-block",
                "text-align": "center"
            }
        ),
        html.Div(
            html.P("article is directed from these articles"),
            style = {
                "width": "48%",
                "font-size": "18px",
                "letter-spacing": "5px",
                "font-family": "monospace",
                "display": "inline-block",
                "text-align": "center"
            }
        ),
        
    ]),
    html.Div([
        html.Div(
            dcc.Graph(
                id = "forwards",
                responsive = True
            ),
            style = {
                "width": "48%",
                "display": "inline-block",
                "border":"3px #5c5c5c solid",
                "padding-top": "5px",
                "padding-right": "1px"
                
            }
        ),
        html.Div(style = {
                "width": "2%",
                "display": "inline-block",
                "padding-top": "5px"
                # "border":"9px gray solid",
                # "padding": "10px"
            }),
        html.Div(
            dcc.Graph(
                id = "backwards",
                responsive = True
            ),
            style = {
                "width": "48%",
                "display": "inline-block",
                "border":"3px #5c5c5c solid",
                "padding-top": "5px",
                "padding-left": "1px"
                # "padding": "2px"
            }
        )
    ])
])

# art = art_from_origin(prop_params = "linkshere")
# _, _ = create_random_populated_sphere(radius=1000, points=art, plot_flag=True, show_lines_with_origin=True)

@app.callback([
    dash.dependencies.Output("forwards", "figure"),
    dash.dependencies.Output("backwards", "figure")
],
    dash.dependencies.Input("art_link", "value")
)
def update_output(art_link):
    
    # article_name = art_link.split("/")[-1]
    # # print(article_name)
    # art = art_from_origin(prop_params = "links", article_name = article_name)
    # # print(art)
    # forwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True)

    # art = art_from_origin(prop_params = "linkshere", article_name = article_name)
    # backwards = create_random_populated_sphere(radius=100, points=art, plot_flag=False, show_lines_with_origin=True, dot_color="#ff3b3b")

    forwards = helpers(
        link = art_link,
        prop_params = "links"
    )
    forwards = forwards.plot_points()
    
    backwards = helpers(
        link = art_link,
        prop_params = "linkshere"
    )
    backwards = backwards.plot_points(dot_color="#ff3b3b")
    

    return (forwards, backwards)


def run(port=8050, host='127.0.0.1', debug = False):
    app.run_server(debug = debug, port=port, host = host)

if __name__ == "__main__":
    run()