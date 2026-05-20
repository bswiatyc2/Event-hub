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
from app.models import Event, Category
from datetime import datetime

@bp.route('/')
def index():
    """List upcoming events.

    HW9: query Event for rows with starts_at >= now, ordered by starts_at,
    and render events/index.html with them.
    """
    # TODO (HW9)
    now = datetime.utcnow()
    events = Event.query.filter(Event.starts_at >= now)\
        .order_by(Event.starts_at.asc())\
        .all()
    return render_template('events/index.html', title='Events', events=events)


@bp.route('/<int:event_id>')
def detail(event_id):
    """Public event detail page.

    HW9: fetch the event by id (use db.session.get or get_or_404), render
    events/detail.html with the event and its categories.
    """
    # TODO (HW9)
    event = db.session.get(Event, event_id) or abort(404)
    return render_template('events/detail.html',
                           title=event.title, event=event)


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
    categories = Category.query.order_by(Category.name).all()
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            location=form.location.data,
            description=form.description.data,
            starts_at=form.starts_at.data,
            ends_at=form.ends_at.data,
            creator=current_user,
        )

        selected_ids = request.form.getlist('category_ids')
        event.categories = Category.query.filter(
            Category.id.in_(selected_ids)
        ).all()

        db.session.add(event)
        db.session.commit()
        flash(f'Event {event.title} created!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))
    return render_template('events/form.html', form=form, categories=categories, mode='create')
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
    event = db.session.get(Event, event_id) or abort (404)
    if event.creator_id != current_user.id:
        abort(403)

    catagories = Category.query.order_by(Category.name).all()
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.location = form.location.data
        event.starts_at = form.starts_at.data
        event.ends_at = form.ends_at.data

        selected_ids = request.form.getlist('category_ids')
        event.categories = Category.query.filter(
            Category.id.in_(selected_ids)
        ).all()

        db.session.commit()
        flash(f'Event {event.title} updated!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))
    return render_template('events/form.html', title='Edit event',
                           event=event, mode='edit')




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
    event = db.session.get(Event, event_id) or abort(404)
    if event.creator_id != current_user.id:
        abort(403)

    db.session.delete(event)
    db.session.commit()
    flash(f'Event {event.title} deleted!', 'success')
    return redirect(url_for('events.index'))

