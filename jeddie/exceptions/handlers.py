from flask import flash, redirect

from exceptions.exceptions import InvalidRSVPException
from routes.frontend import bp


@bp.errorhandler(InvalidRSVPException)
def invalid_rsvp(e):
    if e.message:
        flash(e.message)
    return redirect('jeddie.rsvp')