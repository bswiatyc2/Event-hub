"""EventHub models.

`User` is provided complete (lifted from StudyStack). The remaining models
are stubs that you implement as part of HW9. Follow Week 9's lecture as the
reference implementation.
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


# ----------------------------------------------------------------------------
# Category  -- TODO (HW9)
#
# Required columns:
#   id    : Integer, primary key
#   name  : String(50), unique, not null  (e.g. "Tech")
#   slug  : String(50), unique, not null  (e.g. "tech")
# Hint: see the lecture, Part 4 ("Category").
# ----------------------------------------------------------------------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

# ----------------------------------------------------------------------------
# event_categories  -- TODO (HW9)
#
# Pure association table (no extra data) connecting events <-> categories.
# Use db.Table(...) with two columns, both primary_key=True:
#   event_id     -> event.id
#   category_id  -> category.id
# ----------------------------------------------------------------------------
event_categories = db.Table(
    'event_categories',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'),
              primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'),)

)


# ----------------------------------------------------------------------------
# Event  -- TODO (HW9)
#
# Required columns:
#   id, title, description, location, starts_at, ends_at, created_at, creator_id
# Required relationships:
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
# ----------------------------------------------------------------------------
# RSVP  -- TODO (HW9)
#
# Through-table WITH extra columns. Required:
#   id, status (default 'attending'), created_at
#   event_id  -> event.id
#   user_id   -> user.id
# Required:
#   __table_args__ with a UniqueConstraint('event_id', 'user_id',
#                                          name='uq_rsvp_event_user')
# Required relationship:
#   user (backref='rsvps')   -- the inverse Event.rsvps comes from Event side
# ----------------------------------------------------------------------------
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
