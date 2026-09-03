from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app import db
from app.events import bp
from app.events.forms import EventForm
from app.models import Event, Category
from datetime import datetime

@bp.route('/')
def index():
    now = datetime.utcnow()
    events = Event.query.filter(Event.starts_at >= now)\
        .order_by(Event.starts_at.asc())\
        .all()
    return render_template('events/index.html', title='Events', events=events)


@bp.route('/<int:event_id>')
def detail(event_id):
    event = db.session.get(Event, event_id) or abort(404)
    return render_template('events/detail.html',
                           title=event.title, event=event)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new event.
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


@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    """Edit an existing event. Only the creator may edit.
    """
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
                           form=form, event=event, mode='edit', categories=catagories)




@bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
def delete(event_id):
    event = db.session.get(Event, event_id) or abort(404)
    if event.creator_id != current_user.id:
        abort(403)

    db.session.delete(event)
    db.session.commit()
    flash(f'Event {event.title} deleted!', 'success')
    return redirect(url_for('events.index'))

