"""Nox sessions."""
import nox


@nox.session(python=["3.7", "3.9", "3.11"])
def tests(session):
    """Run tests."""
    session.run("poetry", "install", external=True)
    session.run("pytest", "-svvv", "tests")
