import os

from nox import Session, options, session

python_packages = ["api"]

options.sessions = ["test"]
options.default_venv_backend = "none"

python_package_paths = [
    os.path.join("packages", package) for package in python_packages
]


@session
def test(session: Session):
    session.notify("test:format")
    session.notify("test:lint")
    session.notify("test:type")
    session.notify("test:unit")


@session(name="test:ci")
def test_ci(session: Session):
    session.notify("test:format")
    session.notify("test:lint")
    session.notify("test:type")
    session.run("pytest", *python_package_paths)


@session(name="test:e2e")
def test_e2e(session: Session):
    session.run("pytest", "-k", "e2e", *python_package_paths)


@session(name="test:format")
def test_format(session: Session):
    session.run("black", "--check", *python_package_paths)


@session(name="test:integration")
def test_integration(session: Session):
    session.run("pytest", "-k", "integration", *python_package_paths)


@session(name="test:lint")
def test_lint(session: Session):
    session.run("ruff", *python_package_paths)


@session(name="test:type")
def test_type(session: Session):
    session.run("pyright", *python_package_paths)


@session(name="test:unit")
def test_unit(session: Session):
    session.run("pytest", "-k", "unit", *python_package_paths)


@session(name="test:ci")
def test_ci(session: Session):
    session.run("kubectl", "apply", "-f", "manifests/ci/test.yml", external=True)
    try:
        session.run(
            "kubectl", "wait", "--for=condition=complete", "job/ci-test", external=True
        )
    finally:
        session.run("kubectl", "delete", "-f", "manifests/ci/test.yml")
