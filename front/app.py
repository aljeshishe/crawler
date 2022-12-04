import io

import boto3
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from flask import Flask

from settings import settings


def read_data():
    key = f'data.csv'
    s3_client = boto3.client("s3")
    try:
        response = s3_client.get_object(Bucket=settings.AWS_S3_BUCKET, Key=key)
        status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        assert status_code == 200, f"HTTPStatusCode={status_code} expected:200"
        df = pd.read_csv(io.BytesIO(response["Body"].read()))
    except s3_client.exceptions.NoSuchKey as e:
        df = pd.DataFrame(columns=['dt', 'count'])
    return df

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

df = read_data()
df["dt"] = pd.to_datetime(df["dt"])
df = df.set_index('dt').resample("D").mean()
figure = px.line(df, x=df.index, y="count")

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
                html.H4(children="hh.ru python developers count"),
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
