import nox

PACKAGE_NAME = "spotifyfavouritesmanager"
PACKAGE_FILES = [PACKAGE_NAME, "noxfile.py"]


@nox.session
def lint(session):
    session.install("flake8", "black", "mypy")
    session.run("mypy", PACKAGE_NAME)
    session.run("flake8", *PACKAGE_FILES)
    session.run("black", "--check", *PACKAGE_FILES)


@nox.session
def format(session):
    session.install("black", "isort")
    session.run("isort", "--recursive", *PACKAGE_FILES)
    session.run("black", *PACKAGE_FILES)
