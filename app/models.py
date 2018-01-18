from sqlalchemy.ext.hybrid import hybrid_property

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    auroras = db.relationship('AuroraConfig', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class AuroraConfig(db.Model):
    __tablename__ = 'aurora_config'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ip_address = db.Column(db.String(16))
    port = db.Column(db.Integer)
    token = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Aurora %r>' % self.name

    @hybrid_property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @hybrid_property
    def effects(self):
        return self._effects

    @effects.setter
    def effects(self, effects):
        self._effects = effects

    @hybrid_property
    def selected_effect(self):
        return self._selected_effect

    @selected_effect.setter
    def selected_effect(self, effect):
        self._selected_effect = effect

    @hybrid_property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        self._brightness = brightness