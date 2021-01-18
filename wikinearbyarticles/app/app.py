import dash
import dash_core_components as dcc
import dash_html_components as html
import requests

from wikinearbyarticles.bin.wna import wna

# TODO add animations
# TODO between graphs as they are updated, extending graphs
fw_points_global = {}
bw_points_global = {}

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    # external_stylesheets=[dbc.themes.DARKLY]
    external_stylesheets=external_stylesheets,
)

net_layout = {
    "height": 1200,
    "width": 800,
    "hoverlabel": {
        "font": {"family": "monospace"},
        # "hover"
    },
    # template = "plotly_dark",
    "font": {"family": "monospace", "size": 18},
    "scene": {
        "xaxis": {"visible": False, "showticklabels": False},
        "yaxis": {"visible": False, "showticklabels": False},
        "zaxis": {"visible": False, "showticklabels": False},
    },
    "margin": {
        "pad": 0,
        "t": 0,
        "r": 0,
        "l": 0,
        "b": 0,
    },
}

app.layout = html.Div(
    [
        html.Div(
            html.P(
                "wiki nearby articles",
                style={
                    "font-size": "72px",
                    "fontFamily": "monospace",
                    "letter-spacing": "5px",
                    "text-align": "center",
                    "font-weight": "light",
                    "color": "#525252",
                },
            )
        ),
        html.Div(html.Hr()),
        html.Div(
            html.P("enter article link below"),
            style={
                "font-size": "13px",
                "letter-spacing": "2px",
                "fontFamily": "monospace",
                "margin": "0  auto",
                "display": "center",
                "width": "100%",
                "text-align": "center",
                # 'padding-left':'10%', 'padding-right':'10%',
                "border": "none",
                "border-bottom": "0px solid #5c5c5c",
                # "background-color": "#1a1a1a",
                "color": "#9c9c9c",
                "padding-bottom": "3px",
            },
        ),
        html.Div(
            [
                dcc.Input(
                    id="art_link",
                    className="text_input",
                    # placeholder = "enter wikipedia article link",
                    value="https://en.wikipedia.org/wiki/MissingNo.",
                    style={
                        "font-size": "18px",
                        "fontFamily": "monospace",
                        "margin": "0  auto",
                        "display": "center",
                        "width": "100%",
                        "text-align": "center",
                        "text-spacing": "1px",
                        # 'padding-left':'10%', 'padding-right':'10%',
                        "border": "none",
                        "border-bottom": "0.5px solid #5c5c5c",
                        # "background-color": "#1a1a1a",
                        "color": "#525252",
                        "padding-bottom": "3px",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    html.P(id="main-article-summary"),
                    style={
                        "font-size": "17px",
                        "letter-spacing": "2px",
                        "fontFamily": "monospace",
                        "margin": "0  auto",
                        "display": "center",
                        "width": "60%",
                        "text-align": "center",
                        # 'padding-left':'10%', 'padding-right':'10%',
                        "border": "none",
                        "color": "#5e5e5e",
                        # "padding-bottom": "3px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                        "padding-top": "10px",
                    },
                )
            ]
        ),
        html.Div(html.Br()),
        html.Div(
            [
                html.Div(
                    html.P("article directs to these articles"),
                    style={
                        "width": "100%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="choose-section-forward",              ),
                    style={
                        "width": "10%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    dcc.Dropdown(
                        id="points-fw",
                        placeholder = "expand articles"
                    ),
                    style={
                        "width": "90%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
            ]
        ),
        html.Div(html.Br()),
        html.Div(
            [
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id="forwards",
                            responsive=True,
                            style={
                                "width": "100%",
                                "height": "100%",
                            },
                        ),
                        style={
                            "width": "100%",
                            "height": "100%",
                        },
                    ),
                    style={
                        "width": "68%",
                        "height": "1000px",
                        "display": "inline-block",
                        "border": "3px #5c5c5c solid",
                        "padding-top": "5px",
                        "padding-left": "1px",
                        "overflow": "hidden",
                    },
                ),
                html.Div(
                    style={
                        "width": "2%",
                        "height": "1000px",
                        "display": "inline-block",
                        "padding-top": "5px",
                        "overflow": "hidden",
                    }
                ),
                html.Div(
                    html.P(id="forward-hover-description"),
                    style={
                        "width": "26%",
                        "font-size": "15.5px",
                        "height": "1000px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                        "overflow": "hidden",
                        "padding-left": "1px",
                    },
                ),
            ]
        ),

        html.Div(
            [
                html.Div(
                    html.P("article is directed from these articles"),
                    style={
                        "width": "100%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="choose-section-backward",
                    ),
                    style={
                        "width": "10%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    dcc.Dropdown(
                        id="points-bw",
                        placeholder = "expand articles"
                    ),
                    style={
                        "width": "90%",
                        "font-size": "18px",
                        "letter-spacing": "5px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
            ]
        ),
        
        html.Div(
            [
                html.Div(
                    html.Div(
                        dcc.Graph(
                            id="backwards",
                            responsive=True,
                            style={"width": "100%", "height": "100%"},
                        ),
                        style={
                            "width": "100%",
                            "height": "100%",
                        },
                    ),
                    style={
                        "width": "68%",
                        "height": "1000px",
                        "display": "inline-block",
                        "border": "3px #5c5c5c solid",
                        "padding-top": "5px",
                        "padding-left": "1px",
                        "overflow": "hidden",
                    },
                ),
                html.Div(
                    html.P(),
                    style={
                        "width": "2%",
                        "display": "inline-block",
                        "text-align": "center",
                    },
                ),
                html.Div(
                    html.P(id="backward-hover-description"),
                    style={
                        "width": "26%",
                        "font-size": "15.5px",
                        "height": "1000px",
                        "font-family": "monospace",
                        "display": "inline-block",
                        "text-align": "center",
                        "margin": "auto",
                        "overflow": "hidden",
                        "padding-left": "1px",
                    },
                ),
            ]
        ),
    ]
)

# this callback will only work when the article link is changed
@app.callback(
    [
        dash.dependencies.Output("forwards", "figure"),
        dash.dependencies.Output("main-article-summary", "children"),
        dash.dependencies.Output("points-fw", "options"),
    ],
    [
        dash.dependencies.Input("art_link", "value"),
        dash.dependencies.Input("points-fw", "value"),
    ],
)
def update_output(art_link, val_fw):

    global fw_points_global

    # TODO this is a temporary solution, fix it
    # TODO this is a temporary solution, fix it
    title = art_link.split("/")[-1]
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "exsentences": "5",
        "exlimit": "1",
        "explaintext": "1",
        "formatversion": "2",
    }
    # print("THIS IS VALUE FORWARDS", val_fw)
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    summary = DATA["query"]["pages"][0]["extract"]

    forwards = wna(link=art_link, prop_params="links", points=fw_points_global)
    forwards.collect_points(center=val_fw)
    fw_points = forwards.return_points(drop=True)
    fw_points = [{"label": item, "value": item} for item in fw_points]

    fw_points_global = forwards.return_points(drop=False)
    forwards = forwards.plot()
    forwards["layout"] = net_layout

    return forwards, summary, fw_points


@app.callback(
    [
        dash.dependencies.Output("backwards", "figure"),
        dash.dependencies.Output("points-bw", "options"),
    ],
    [
        dash.dependencies.Input("art_link", "value"),
        dash.dependencies.Input("points-bw", "value"),
    ],
)
def update_output(art_link, val_bw):

    global bw_points_global

    # TODO this is a temporary solution, fix it
    title = art_link.split("/")[-1]
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "exsentences": "5",
        "exlimit": "1",
        "explaintext": "1",
        "formatversion": "2",
    }
    # print("THIS IS VALUE FORWARDS", val_fw)
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    summary = DATA["query"]["pages"][0]["extract"]

    backwards = wna(link=art_link, prop_params="linkshere", points=bw_points_global)
    backwards.collect_points(center=val_bw)
    bw_points = backwards.return_points(drop=True)
    bw_points = [{"label": item, "value": item} for item in bw_points]

    bw_points_global = backwards.return_points(drop=False)
    backwards = backwards.plot(dot_color="#ff3b3b")
    backwards["layout"] = net_layout

    return backwards, bw_points


@app.callback(
    dash.dependencies.Output("forward-hover-description", "children"),
    dash.dependencies.Input("forwards", "hoverData"),
)
def show_hover_text(data):
    # print(data)
    if data is not None:
        data = data["points"][0]
        if "text" not in data.keys():
            print("hovering on lines")
            text = "hovering on lines"
        else:
            print("hovering on point ", end="")
            art_name = data["text"]
            print(art_name)
            wna_hover = wna(link=art_name, prop_params="links")
            hover = wna_hover.article_summary_for_hover(
                collect_points=False, number_of_lines=8
            )
            # print(hover, type(hover))
            text = hover["query"]["pages"][0]["extract"]
            if text == "":
                text = "no summary available"
            print("got hover data")
    else: 
        text = "Loading..."
    return text


@app.callback(
    dash.dependencies.Output("backward-hover-description", "children"),
    dash.dependencies.Input("backwards", "hoverData"),
)
def show_hover_text(data):
    # try:
    # print(data)
    if data is not None:
        data = data["points"][0]
        if "text" not in data.keys():
            print("hovering on lines")
            text = "hovering on lines"
        else:
            print("hovering on point ", end="")
            art_name = data["text"]
            print(art_name)
            wna_hover = wna(link=art_name, prop_params="linkshere")
            hover = wna_hover.article_summary_for_hover(
                collect_points=False, number_of_lines=8
            )
            # print(hover, type(hover))
            text = hover["query"]["pages"][0]["extract"]
            if text == "":
                text = "no summary available"
            print("got hover data")
    else: 
        text = "Loading..."
    return text


def run(port=8050, host="127.0.0.1", debug=True):
    app.run_server(debug=debug, port=port, host=host)


if __name__ == "__main__":
    run()
