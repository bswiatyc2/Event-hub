# EventHub - Starter Kit (Week 9)

EventHub is the third project in MCON 504. This starter kit gives you a working
Flask scaffold (App Factory in `app/__init__.py`, blueprints as subpackages,
auth lifted from StudyStack, Flask-Migrate configured) so you can spend HW9 on
the new material -- models, migrations, seed data, and CRUD -- instead of
re-typing boilerplate.

Push it to GitHub as a new repository named `eventhub-<your-github-handle>`.

---

## What is EventHub?

A campus / community event platform. Users create events, attach categories,
and RSVP to events created by others. Built across Weeks 9-12:

- **Week 9** (this kit) -- Models, CRUD, migrations
- **Week 10** -- Threaded comments, N+1 query optimization
- **Week 11** -- JSON read API, Bootstrap polish
- **Week 12** -- Token-authenticated write API, deployment

This kit covers Week 9 only. The `app/models.py` ships with **stubs** for
`Category`, `Event`, and `RSVP` -- you fill those in as part of HW9, following
the lecture.

---

## What's already built for you

| File / Folder | Status | Notes |
|---------------|--------|-------|
| `app.py` | Done | Entry point. `from app import create_app, db`. Same pattern as StudyStack. |
| `config.py` | Done | Single `Config` class -- SECRET_KEY, SQLite URI. |
| `app/__init__.py` | Done | `create_app()` factory; defines `db`, `migrate`, `login`, `csrf`. |
| `app/models.py` | **Partial** -- `User` is done, the rest is TODO | Add `Category`, `Event`, `event_categories`, `RSVP`. |
| `app/main/` | Done | `/` redirects to `/events`. |
| `app/auth/` | Done | `/auth/register`, `/auth/login`, `/auth/logout` (lifted from StudyStack). |
| `app/events/` | **Stub** | Routes are sketched with `# TODO`. You implement them in HW9. |
| `app/templates/base.html` | Done | Bootstrap 5 base layout, flash messages, nav. |
| `app/templates/auth/*` | Done | Login + register forms. |
| `app/templates/events/*` | **Stubs** | `index`, `detail`, `form` skeletons. Polish in HW9. |
| `seed.py` | Skeleton | User seeding works; categories, events, and RSVPs are TODO. |
| `migrations/` | Not yet | You will create this with `flask db init`. |

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/<your-handle>/eventhub-<your-handle>.git
cd eventhub-<your-handle>
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Copy the env file

```bash
cp .env.example .env               # Windows: copy .env.example .env
```

Then open `.env` and replace the placeholder `SECRET_KEY` with something
random:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Initialize migrations (once you have the models built)

After you've finished implementing the three new models in `app/models.py`:

```bash
flask db init
flask db migrate -m "initial schema: user, category, event, event_categories, rsvp"
```

**Open the generated file** under `migrations/versions/` and verify:

- All 5 tables (`user`, `category`, `event`, `event_categories`, `rsvp`) appear
- The `uq_rsvp_event_user` unique constraint is in the `rsvp` table
- Foreign keys point at the right parent tables

Then apply it:

```bash
flask db upgrade
```

### 4. Seed test data

```bash
python seed.py
```

You should see output like:

```
Resetting database...
Seeded 4 categories
Seeded 3 users (admin, alice, bob)
Seeded 3 events
Seeded 3 RSVPs

Test login: admin@example.com / password
```

### 5. Run the app

```bash
flask run
```

Visit http://127.0.0.1:5000 -- the home route redirects to `/events`. Log in
as `admin@example.com` / `password` to create events.

---

## Schema overview

```
user                category           event                rsvp
+----+              +----+             +----+               +----+
| id |              | id |             | id |               | id |
| .. |              | .. |             | starts_at         | status
+----+              +----+             | creator_id ---+   | event_id --+
   |                  |                +----+          |   | user_id ---+----+
   |                  |                                |   +----+            |
   |                  |     event_categories           |                     |
   |                  |     +-------------+            |                     |
   |                  +-----| category_id |            |                     |
   |                        | event_id    |------------+                     |
   |                        +-------------+                                  |
   +-----------------------------------------------------------------------+
```

- **Event <-> Category:** many-to-many via `event_categories` (no extra columns)
- **Event <-> User (creator):** one-to-many (`Event.creator_id`)
- **Event <-> User (attendees):** many-to-many **with extra columns** via `RSVP`
  (`status`, `created_at`, plus a unique constraint on `(event_id, user_id)`)

---

## HW9 deliverables (graded)

1. Three models implemented in `app/models.py` matching the lecture
2. `flask db init` + initial migration committed under `migrations/versions/`
3. `python seed.py` runs cleanly on a fresh database and produces the output above
4. `/events/` lists upcoming events
5. `/events/<id>` renders an event detail page including categories
6. `/events/new` (logged-in only) creates events with selected categories
7. `/events/<id>/edit` and `/events/<id>/delete` enforce creator-only access

See [[MCON504 - HW9 - Assignment - EventHub Core Models and CRUD]] for the full rubric.

---

## File tree

```
eventhub/
├── README.md                         <- this file
├── .env.example
├── .gitignore
├── requirements.txt
├── app.py                            <- entry point
├── config.py                         <- Config class
├── seed.py                           <- skeleton; events + RSVPs are HW9
└── app/
    ├── __init__.py                   <- create_app(), db, migrate, login, csrf
    ├── models.py                     <- User done; Category/Event/RSVP TODO
    ├── main/
    │   ├── __init__.py               <- bp = Blueprint('main', __name__)
    │   └── routes.py
    ├── auth/
    │   ├── __init__.py
    │   ├── routes.py                 <- done (from StudyStack)
    │   └── forms.py
    ├── events/
    │   ├── __init__.py
    │   ├── routes.py                 <- TODO stubs to flesh out
    │   └── forms.py                  <- EventForm provided
    └── templates/
        ├── base.html
        ├── auth/
        │   ├── login.html
        │   └── register.html
        └── events/
            ├── index.html
            ├── detail.html
            └── form.html             <- shared by create + edit
```

---

## When you're stuck

1. Re-read [[MCON504 - Week 09 - Lecture - EventHub Models CRUD and Migrations]] --
   every pattern in this kit is covered there.
2. Check the StudyStack repo for the analogous code -- auth, blueprints, ownership
   checks, and many-to-many wiring are nearly identical in shape.
3. Office hours.
