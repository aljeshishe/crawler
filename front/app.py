from dash import Dash, html
from flask import Flask, jsonify, make_response


app = Flask(__name__)



@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!1')


_app = Dash(
    __name__,
    server=app,
)

_app.layout = html.Div(html.H1("Hello Dash22!"))

if __name__ == "__main__":
    app.run(debug=True)
