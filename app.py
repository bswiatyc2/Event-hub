from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models import User, Category, Event, RSVP
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'Event': Event,
        'RSVP': RSVP,
    }


if __name__ == '__main__':
    app.run(debug=True)
