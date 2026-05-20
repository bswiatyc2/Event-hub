"""Populate the development database with realistic test data.

Run with:    python seed.py

WARNING: This script calls db.drop_all(). It will delete every row in every
table. Never run in production.

You finish the events + RSVPs sections in HW9 -- the user and category sections
are already provided as a working reference.
"""
from datetime import datetime, timedelta

from app import create_app, db
from app.models import User, Category, Event, RSVP


app = create_app()

with app.app_context():
    print('Resetting database...')
    db.drop_all()
    db.create_all()

    #---- Categories  -- TODO (HW9, uncomment after building Category) ----
    categories = [
        Category(name='Tech',    slug='tech'),
        Category(name='Art',     slug='art'),
        Category(name='Music',   slug='music'),
        Category(name='Fitness', slug='fitness'),
    ]
    db.session.add_all(categories)
    db.session.flush()  # assign IDs without committing
    print(f'Seeded {len(categories)} categories')

    # ---- Users (provided) ------------------------------------------------
    admin = User(username='admin', email='admin@example.com')
    admin.set_password('password')

    alice = User(username='alice', email='alice@example.com')
    alice.set_password('password')

    bob = User(username='bob', email='bob@example.com')
    bob.set_password('password')

    db.session.add_all([admin, alice, bob])
    db.session.flush()
    print('Seeded 3 users (admin, alice, bob)')

    # ---- Events  -- TODO (HW9) -------------------------------------------
    # Create three Event rows. Use:
    now = datetime.utcnow()
    #starts_at = now + timedelta(days=N)
    # Attach 1-2 categories to each via the .categories list assignment.
    #
    events = [
        Event(
            title='SUMMER FUN',
       description='pool party',
            location='pool',
            starts_at=now + timedelta(days=1),
            ends_at=now + timedelta(days=1),
            creator=admin
        ),
        Event(
            title='TOP SECRET',
            description='secret party',
            location='top',
            starts_at=now + timedelta(days=1),
            ends_at=now + timedelta(days=1),
            creator=alice
        ),
        Event(
            title='Birthday',
            description='celibrate birthday',
            location='park',
            starts_at=now + timedelta(days=1),
            ends_at=now + timedelta(days=1),
            creator=bob
        ),
        Event(
            title='Birthday 2',
            description='celibrate birthday',
            location='park',
            starts_at=now + timedelta(days=1),
            ends_at=now + timedelta(days=1),
            creator=bob
        ),
        Event(
            title='Birthday 3',
            description='celibrate birthday',
            location='park',
            starts_at=now + timedelta(days=1),
            ends_at=now + timedelta(days=1),
            creator=bob
        )

    ]
    db.session.add_all(events)

    events[0].categories = [categories[3]]
    events[1].categories = [categories[0]]
    events[2].categories = [categories[1]]
    events[2].categories = [categories[1]]
    events[2].categories = [categories[1]]

    db.session.flush()
    print(f'Seeded {len(events)} events')


    # ---- RSVPs  -- TODO (HW9) --------------------------------------------
    # Create three RSVP rows tying alice and bob to the events above.
    # Remember: one user can RSVP to a given event only once.
    #
    rsvps = [
        RSVP(user=alice, event_id=events[0].id, status='attending'),
        RSVP(user=alice, event_id=events[1].id,status='attending'),
        RSVP(user=bob, event_id=events[2].id, status='attending'),
        RSVP(user=bob, event_id=events[3].id, status='attending'),
    ]
    db.session.add_all(rsvps)
    db.session.flush()
    print(f'Seeded {len(rsvps)} RSVPs')

    db.session.commit()
    print('\nTest login: admin@example.com / password')
