"""Shared test fixtures — YOUR CODE, Task 5.4.

Two fixtures the API tests (test_columns.py, test_cards.py) rely on:

@pytest.fixture
def test_db():
    Point db at settings.test_database_url (NOT your dev board!), ensure
    tables exist, TRUNCATE users/columns/cards between tests so every test
    starts clean. How you point db there is a design conversation for 5.4 —
    monkeypatch, an env var, or a parameter. Talk it through before coding.

@pytest.fixture
def client(test_db):
    fastapi.testclient.TestClient(main.app) with the auth gate swapped out:
        app.dependency_overrides[auth.get_current_user] = lambda: FAKE_USER
    That's why get_current_user is a dependency and not middleware — tests
    never need Google. Insert FAKE_USER into the users table too (FKs!).

A FAKE_USER dict constant here is also handy for the ownership tests, which
need a SECOND user id that the client is NOT logged in as.
"""

# TODO(Task 5.4): FAKE_USER, test_db fixture, client fixture
