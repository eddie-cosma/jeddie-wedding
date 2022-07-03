import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return flask.render_template("base.html", title="Home")


@app.route('/test')
def test():
    from middleware import sheets

    guest_list = sheets.RsvpList()
    return guest_list.update("Postal Code", "90210", "Invitation Code", "339028")
