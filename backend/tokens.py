"""ID-token verification — YOUR CODE, Task 3 (a port, not a rewrite).

Port from ../GoogleOAuthProject/app/tokens.py. Before porting, be able to answer:
what attack does each of the four checks block?
  signature (JWKS) / iss / aud / exp        (KNOWLEDGE.md there, section 5)

Contract auth.py (Task 4) will call:
    verify_id_token(id_token: str) -> dict   # verified claims; raises on any failure
"""

# TODO(Task 3.2): port from GoogleOAuthProject
