"""App configuration — YOUR CODE, Task 1.3.

Contract (other modules rely on this):
    from config import settings
    settings.google_client_id      (str)
    settings.google_client_secret  (str)
    settings.session_secret        (str)
    settings.database_url          (str)
    settings.test_database_url     (str)
    settings.redirect_uri          (str)

Approach: a pydantic-settings `BaseSettings` subclass that reads backend/.env.
Why not os.environ reads scattered around the code? One validated object,
loud failure at startup if a variable is missing, one place to see every knob.
"""

# TODO(Task 1.3): implement Settings and create the single `settings` instance.
