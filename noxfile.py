import os

from nox import Session, options, session

typescript_packages = ["frontend"]
python_packages = ["api"]

options.sessions = ["test"]
options.default_venv_backend = "none"

python_package_paths = [
    os.path.join("packages", package) for package in python_packages
]
typescript_package_paths = [
    os.path.join("packages", package) for package in typescript_packages
]


@session
def test(session: Session):
    session.notify("test:format")
    session.notify("test:lint")
    session.notify("test:type")
    session.notify("test:unit")


@session(name="test:e2e")
def test_e2e(session: Session):
    session.notify("test:e2e:backend")
    session.notify("test:e2e:frontend")


@session(name="test:e2e:backend")
def test_e2e_backend(session: Session):
    session.run("pytest", "-k", "e2e", *python_package_paths)


@session(name="test:e2e:frontend")
def test_e2e_frontend(session: Session):
    session.run("yarn", "jest", "--group=e2e", external=True)


@session(name="test:format")
def test_format(session: Session):
    session.notify("test:format:backend")
    session.notify("test:format:frontend")


@session(name="test:format:backend")
def test_format_backend(session: Session):
    session.run("black", "--check", *python_package_paths)


@session(name="test:format:frontend")
def test_format_frontend(session: Session):
    session.run("yarn", "prettier", "--check", *typescript_package_paths, external=True)


@session(name="test:integration")
def test_integration(session: Session):
    session.notify("test:integration:backend")
    session.notify("test:integration:frontend")


@session(name="test:integration:backend")
def test_integration_backend(session: Session):
    session.run("pytest", "-k", "integration", *python_package_paths)


@session(name="test:integration:frontend")
def test_integration_frontend(session: Session):
    session.run("yarn", "jest", "--group=integration", external=True)


@session(name="test:lint")
def test_lint(session: Session):
    session.notify("test:lint:backend")
    session.notify("test:lint:frontend")


@session(name="test:lint:backend")
def test_lint_backend(session: Session):
    session.run("ruff", *python_package_paths)


@session(name="test:lint:frontend")
def test_lint_frontend(session: Session):
    session.run("yarn", "eslint", *typescript_package_paths, external=True)


@session(name="test:type")
def test_type(session: Session):
    session.notify("test:type:backend")
    session.notify("test:type:frontend")


@session(name="test:type:backend")
def test_type_backend(session: Session):
    session.run("pyright", *python_package_paths)


@session(name="test:type:frontend")
def test_type_frontend(session: Session):
    for package in typescript_package_paths:
        with session.cd(package):
            session.run(
                "yarn",
                "tsc",
                "--noEmit",
                external=True,
            )


@session(name="test:unit")
def test_unit(session: Session):
    session.notify("test:unit:backend")
    session.notify("test:unit:frontend")


@session(name="test:unit:backend")
def test_unit_backend(session: Session):
    session.run("pytest", "-k", "unit", *python_package_paths)


@session(name="test:unit:frontend")
def test_unit_frontend(session: Session):
    session.run("yarn", "jest", "--group=unit", external=True)
