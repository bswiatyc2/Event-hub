"""EventHub models.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


# ----------------------------------------------------------------------------
# User (provided)
# ----------------------------------------------------------------------------
class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email         = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

event_categories = db.Table(
    'event_categories',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'),
              primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'),primary_key=True)

)


# ----------------------------------------------------------------------------
# Event
# columns:
#   id, title, description, location, starts_at, ends_at, created_at, creator_id
# relationships:
#   categories  : many-to-many through event_categories
#   rsvps       : one-to-many, with cascade='all, delete-orphan'
#   creator     : many-to-one to User (backref='events_created')
# ----------------------------------------------------------------------------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    starts_at = db.Column(db.DateTime, nullable=False, index=False)
    ends_at = db.Column(db.DateTime, nullable=True, index=False)
    creator = db.relationship('User', backref='events_created')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    category = db.relationship(
        'Category',
        secondary=event_categories,
        backref='events',
        lazy='subquery'
    )
    rsvps = db.relationship(
        'RSVP',
        backref='events',
        lazy=True,
        cascade='all, delete-orphan'
    )
    def __repr__(self):
        return f'<Event {self.title}>'

class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='attending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref='rsvps')

    __table_args__ = (
        db.UniqueConstraint('event_id', 'user_id', name='uq_rsvp_event_user'),)
    def __repr__(self):
        return f'<RSVP events={self.event_id} user={self.user_id} status={self.status}>'
