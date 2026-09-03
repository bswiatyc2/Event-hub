# EventHub

A full-stack event management web app built with Flask. Users can register an account, create and manage events, tag them with categories, and browse upcoming events in the community.

## Features

- **User authentication** — registration, login, and logout with hashed passwords (Flask-Login + Werkzeug security)
- **Event CRUD** — create, view, edit, and delete events, with permission checks so only an event's creator can edit or delete it
- **Categories** — many-to-many relationship between events and categories, with a multi-select checkbox UI
- **RSVPs** — data model in place for users to RSVP to events, with a unique constraint preventing duplicate RSVPs
- **Form validation with visible feedback** — every form field shows inline, field-specific error messages (e.g. "Field must be at least 8 characters long") using a reusable Jinja macro
- **Database migrations** — schema changes tracked and applied with Flask-Migrate / Alembic

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate
- **Database:** SQLite
- **Frontend:** Jinja2 templates, Bootstrap 5
- **Auth:** Werkzeug password hashing, session-based login via Flask-Login

## Project Structure

```
app/
├── auth/                 # Registration, login, logout routes + forms
├── events/               # Event CRUD routes + forms
├── main/                 # Landing page routes
├── templates/
│   ├── auth/             # Login and registration pages
│   ├── events/           # Event list, detail, and create/edit form
│   ├── base.html         # Shared page layout
│   └── _macros.html      # Reusable field-rendering macro (label + input + errors)
├── models.py             # SQLAlchemy models: User, Event, Category, RSVP
└── __init__.py           # App factory
migrations/                # Alembic migration history
app.py                     # Entry point
requirements.txt
```

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/bswiatyc2/EventHub.git
   cd EventHub
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   copy .env.example .env      # Windows
   ```
   Fill in a `SECRET_KEY` and any other required values in `.env`.

4. **Set up the database**
   ```bash
   python -m flask db upgrade
   ```

5. **Run the app**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

## Design Notes

- **Reusable form rendering:** rather than repeating the label/input/error-display markup for every form field, a single Jinja macro (`render_field`) handles it generically — including conditionally applying Bootstrap's `is-invalid` class so validation errors are actually visible to the user, not just present in the HTML.
- **Authorization checks:** editing and deleting an event are restricted to that event's creator (`abort(403)` otherwise), enforced at the route level rather than relying on the UI to hide buttons.
- **Composite primary key:** the `event_categories` association table uses a composite primary key (`event_id` + `category_id` together) so the same event/category pairing can never be duplicated.

## Future Improvements

- Build out the RSVP flow in the UI (the data model already supports it)
- Add search/filtering on the events list by category or date range
- Add pagination for the events index
