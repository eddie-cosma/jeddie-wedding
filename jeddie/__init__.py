import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return flask.render_template("base.html", title="Home")


@app.route('/test')
def test():
    from middleware import sheets

    guestlist = sheets.RsvpList()
    return guestlist.update(guestlist.RangeName.rsvp, 1, '2')
