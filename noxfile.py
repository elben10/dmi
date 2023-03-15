from nox import Session, options, session

src_files = ["noxfile.py", "packages/api/dmi"]
test_files = ["packages/api/test_api"]

options.sessions = ["test"]
options.default_venv_backend = "none"


@session
def test(session: Session):
    session.notify("test:format")
    session.notify("test:lint")
    session.notify("test:sort")
    session.notify("test:type")
    session.notify("test:unit")


@session(name="test:e2e")
def test_e2e(session: Session):
    session.run("pytest", "-k", "e2e", *test_files)


@session(name="test:format")
def test_format(session: Session):
    session.run("black", "--check", *src_files, *test_files)


@session(name="test:integration")
def test_integration(session: Session):
    session.run("pytest", "-k", "integration", *test_files)


@session(name="test:lint")
def test_lint(session: Session):
    session.run("ruff", *src_files)


@session(name="test:sort")
def test_sort(session: Session):
    session.run("isort", "--check", *src_files, *test_files)


@session(name="test:type")
def test_type(session: Session):
    session.run("pyright", *src_files, *test_files)


@session(name="test:unit")
def test_unit(session: Session):
    session.run("pytest", "-k", "unit", *test_files)
