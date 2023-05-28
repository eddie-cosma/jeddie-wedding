from flask import flash, redirect, url_for, Blueprint

from exceptions.exceptions import InvalidRSVPException

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(InvalidRSVPException)
def invalid_rsvp(e):
    if e.message:
        flash(e.message)
    return redirect(url_for('jeddie.rsvp'))
