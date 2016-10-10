# -*- coding: utf8 -*-

from flask.ext.login import current_user
from app import db
from app.utils.db import ModelBase, MutableDict
import datetime
import os


class Picture(db.Model, ModelBase):

    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', onupdate='NO ACTION'))

    attributes = db.Column(MutableDict.as_mutable(db.PickleType))

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):  # pragma: no cover
        return '<Picture %r>' % (self.id)


    def save_file(self, fileObj):
        import hashlib
        extension = fileObj.filename.split('.')[-1]

        h = hashlib.new('md5')
        h.update(fileObj.filename)
        h.update(datetime.datetime.utcnow().isoformat())

        self.name = u'%s.%s' % (h.hexdigest(), extension)

        fileObj.save(os.path.join('app/static/uploads', self.name))

    @property
    def image_url(self):
        return os.path.join('/static/uploads', self.name)

    @property
    def name(self):
        return self.get_attribute('name', '')

    @name.setter
    def name(self, value):
        return self.set_attribute('name', value)

    def is_mine(self):
        return current_user.is_authenticated and self.user.id == current_user.id

    def can_edit(self):
        return current_user.is_authenticated and (self.user.id == current_user.id or current_user.is_admin())