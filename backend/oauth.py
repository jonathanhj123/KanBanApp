"""The OAuth dance — YOUR CODE, Task 3 (a port, not a rewrite).

Port from ../GoogleOAuthProject/app/oauth.py AFTER re-reading it and explaining
each function out loud (plan step 3.1). Only the config wiring changes:
redirect_uri now comes from settings.redirect_uri.

Contract auth.py (Task 4) will call:
    make_state() -> str                      # random CSRF token
    make_pkce_pair() -> (verifier, challenge)  # challenge = base64url(sha256(verifier))
    build_auth_url(state, code_challenge) -> str
    exchange_code(code, code_verifier) -> dict   # Google's token response
(If the originals use different names, keep THEIR names and update the plan's
Task 3 Interfaces block so the plan stays truthful.)
"""

# TODO(Task 3.2): port from GoogleOAuthProject
