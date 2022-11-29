import awsgi
from dash import Dash, Input, Output, html, dcc

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


def endpoint(event, context):
    return awsgi.response(app.server, event, context)


if __name__ == '__main__':
    app.run_server(debug=True)
