# api/index.py
# Reuse your existing app defined in app.py (at repo root)
from app import app as flask_app

# Vercel's Python runtime looks for a variable named `app`
# that is a WSGI (or ASGI) application.
app = flask_app
