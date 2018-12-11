
from flask_babel import lazy_gettext as _lg
from app.models import User, GuestUser
import app
import flask


# add our view as the login view to finish configuring the LoginManager
app.login_manager.login_view = "sessions.login"
app.login_manager.login_message = _lg('APP_LOGIN_WARNING_MESSAGE')
app.login_manager.anonymous_user = GuestUser


@app.login_manager.user_loader
def load_user(userid):
    return User.get_by_id(userid)


@app.login_manager.unauthorized_handler
def unauthorized():
    flask.session['redirect_to'] = flask.request.url
    flask.flash(_lg('APP_SIGNIN_WARNING_MESSAGE'), 'error')
    return flask.redirect(flask.url_for('sessions.login'))
