import io

import boto3
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from flask import Flask

from settings import settings


def read_data(file):
    s3_client = boto3.client("s3")
    try:
        response = s3_client.get_object(Bucket=settings.AWS_S3_BUCKET, Key=file)
        status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        assert status_code == 200, f"HTTPStatusCode={status_code} expected:200"
        df = pd.read_csv(io.BytesIO(response["Body"].read()))
        df["dt"] = pd.to_datetime(df["dt"])
        df = df.set_index('dt').groupby("name").resample("D").mean().reset_index()
    except (s3_client.exceptions.NoSuchKey, s3_client.exceptions.NoSuchBucket) as e:
        df = pd.DataFrame(columns=['dt', 'value', "name"])
    return df


server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Statistics dashboard"

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

df = read_data(file="hh.csv")
hh_figure = px.line(df, x="dt", y="value", color="name")

df = read_data(file="linkedin.csv")
linkedin_figure = px.line(df, x="dt", y="value", color="name")

df = read_data(file="bazaraki.csv")
bazaraki_figure = px.line(df, x="dt", y="value", color="name")

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
                html.H4(children="Statistics dashboard"),
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
                                html.P(f"hh.ru"),
                                dcc.Graph(id='hh-graph', figure=hh_figure),
                                html.P(f"linkedin.com"),
                                dcc.Graph(id='linkedin-graph', figure=linkedin_figure),
                                html.P(f"bazaraki.com"),
                                dcc.Graph(id='bazaraki-graph', figure=bazaraki_figure)
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
