import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from flask import Flask


server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "hh.ru python developers count"


mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# App layout
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
figure = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
figure.update_layout(
    dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            center=dict(
                lat=38.72490, lon=-95.61446
            ),
            pitch=0,
            zoom=3.5,
        ),
        autosize=True
    )
)

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.A(
                    html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                    href="https://plotly.com/dash/",
                ),
                html.A(
                    html.Button("Enterprise Demo", className="link-button"),
                    href="https://plotly.com/get-demo/",
                ),
                html.A(
                    html.Button("Source Code", className="link-button"),
                    href="https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-opioid-epidemic",
                ),
                html.H4(children="Rate of US Poison-Induced Deaths"),
                html.P(
                    id="description",
                    children=dcc.Markdown(),
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    f"Heatmap of age adjusted mortality rates from poisonings in year",
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id='example-graph',
                                    figure=figure
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
