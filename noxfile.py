from nox import Session, options
from nox_uv import session


options.default_venv_backend = "uv"
options.reuse_existing_virtualenvs = True

PY_VERS = ["3.12"]


@session(
    python=PY_VERS,
    uv_groups=["dev"],
)
def ruff(s: Session) -> None:
    s.run("ruff", "check", "src", "tests", "noxfile.py")
    s.run("ruff", "format", "src", "tests", "noxfile.py")
