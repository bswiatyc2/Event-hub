"""Events blueprint -- STUB.

You implement the bodies of the routes below as part of HW9. The shape of
each route mirrors the Week 8 `decks` blueprint from StudyStack.

Reference: [[MCON504 - Week 09 - Lecture - EventHub Models CRUD and Migrations]]
"""
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app import db
from app.events import bp
from app.events.forms import EventForm
# from app.models import Event, Category   # uncomment after you build the models


@bp.route('/')
def index():
    """List upcoming events.

    HW9: query Event for rows with starts_at >= now, ordered by starts_at,
    and render events/index.html with them.
    """
    # TODO (HW9)
    events = []
    return render_template('events/index.html', title='Events', events=events)


@bp.route('/<int:event_id>')
def detail(event_id):
    """Public event detail page.

    HW9: fetch the event by id (use db.session.get or get_or_404), render
    events/detail.html with the event and its categories.
    """
    # TODO (HW9)
    abort(404)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new event.

    HW9:
      - On GET, show events/form.html with an empty EventForm and the full
        list of Category rows for the multi-select.
      - On POST, validate the form, build an Event from form fields, attach
        the selected categories via event.categories = [...], commit, and
        redirect to the detail page.
    """
    # TODO (HW9)
    # categories = Category.query.order_by(Category.name).all()
    form = EventForm()
    if form.validate_on_submit():
        flash('TODO: implement create()', 'warning')
        return redirect(url_for('events.index'))
    return render_template('events/form.html', title='New event',
                           form=form, mode='create', categories=[])


@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    """Edit an existing event. Only the creator may edit.

    HW9:
      - Fetch the event; abort(403) if event.creator_id != current_user.id.
      - Pre-populate EventForm with the existing event.
      - On POST, update the columns, replace event.categories with the new
        selection, commit, and redirect to the detail page.
    """
    # TODO (HW9)
    abort(404)


@bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
def delete(event_id):
    """Delete an event. Only the creator may delete.

    HW9:
      - Fetch the event; abort(403) if event.creator_id != current_user.id.
      - db.session.delete(event); db.session.commit().
      - cascade='all, delete-orphan' on Event.rsvps removes the RSVPs.
      - Redirect to the events index.
    """
    # TODO (HW9)
    abort(404)
