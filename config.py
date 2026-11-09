import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _database_uri():
    """Use DATABASE_URL (e.g. PostgreSQL) if set, otherwise a local SQLite file
    so the project runs anywhere with no database setup."""
    url = os.environ.get("DATABASE_URL", "").strip()

    if url:
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    return "sqlite:///" + os.path.join(BASE_DIR, "careconnect.db")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "careconnect-dev-secret-key"

    SQLALCHEMY_DATABASE_URI = _database_uri()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
