# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField, PasswordField, HiddenField, validators
from flask_babel import lazy_gettext as _lg


class LoginForm(FlaskForm):
    email = TextField(_lg('USER_EMAIL'), [
                      validators.Email(), validators.Length(min=10, max=255)])
    password = PasswordField(_lg('USER_PASSWORD'), [validators.Required()])
    remember_me = BooleanField('remember_me', default=False)
    back_link = HiddenField()

    def __init__(self, ret=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if not self.is_submitted() and ret:
            self.back_link.data = ret
