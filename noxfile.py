import nox
import nox.sessions

PACKAGE_NAME = "spotifyfavouritesmanager"
PACKAGE_FILES = [PACKAGE_NAME, "noxfile.py"]


@nox.session
def lint(session: nox.sessions.Session) -> None:
    session.install(
        "flake8==3.7.9", "flake8-import-order==0.18.1", "black==19.10b0", "mypy==0.770"
    )
    session.run("mypy", PACKAGE_NAME)
    session.run("flake8", *PACKAGE_FILES)
    session.run("black", "--check", *PACKAGE_FILES)


@nox.session
def format(session: nox.sessions.Session) -> None:
    session.install("black==19.10b0", "isort==4.3.21")
    session.run("isort", "--recursive", *PACKAGE_FILES)
    session.run("black", *PACKAGE_FILES)
