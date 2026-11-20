"""Custom setuptools build for omnigent.

Generates ``omnigent/_build_info.py`` at wheel build time so the
CLI's update-check (``omnigent/update_check.py``) can tell the user
when their installed build is stale without having to consult
``git`` or hit a remote endpoint at startup.

All other build configuration lives in ``pyproject.toml``; this
file exists solely to register the cmdclass override that runs the
generator before ``build_py`` copies sources into the wheel.

The generated file is gitignored — it is recreated on every build
and only meaningful at install time, where it travels inside the
wheel alongside the rest of the package.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class _GenerateBuildInfo(build_py):
    """Subclass of ``build_py`` that writes ``_build_info.py``.

    The override is the smallest possible intervention: run the
    generator, then defer to the stock ``build_py`` to copy sources
    (including the freshly-written ``_build_info.py``) into the
    wheel's build directory. No other behavior of the build is
    changed.
    """

    def run(self) -> None:
        """Generate ``_build_info.py``, then run build_py."""
        self._write_build_info()
        super().run()
        self._bundle_examples()
        self._bundle_scripts()

    def _bundle_scripts(self) -> None:
        """Copy top-level maintenance scripts into package resources."""
        import shutil

        root = Path(__file__).resolve().parent
        src = root / "scripts" / "uninstall_oss.sh"
        if not src.is_file():
            return
        dest = Path(self.build_lib) / "omnigent" / "resources" / "scripts" / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    def _bundle_examples(self) -> None:
        """Copy bundled example agents into the wheel as real directories.

        ``omnigent/resources/examples/{polly,debby}`` may exist as symlinks
        into the top-level ``examples/`` tree (or not at all) depending on
        the checkout, and setuptools' ``package-data`` never materializes
        symlinks into the built wheel — a directory symlink is not walked.
        A plain ``pip install`` / ``uv tool install`` would then ship a
        package whose ``omnigent.resources.examples`` has no ``polly`` /
        ``debby`` subdir, and bare ``omnigent`` (first-run default → polly)
        dies with "Agent path not found".

        Fix: after ``build_py`` has populated ``build_lib``, copy the real
        example trees from the top-level ``examples/`` dir (present in every
        checkout) into
        ``build_lib/omnigent/resources/examples/<name>`` so every wheel is
        self-contained. This honors the contract documented in cli.py's
        ``_bundled_polly_path``: a symlink in a checkout, a real directory in
        an installed wheel. Editable installs (``uv sync``) resolve the
        in-checkout symlink directly and don't need this.
        """
        import shutil

        root = Path(__file__).resolve().parent
        dest_root = Path(self.build_lib) / "omnigent" / "resources" / "examples"
        for name in ("debby", "polly", "symbiosis"):
            src = root / "examples" / name
            if not src.is_dir():
                continue
            dst = dest_root / name
            if dst.is_symlink() or dst.is_file():
                dst.unlink()
            elif dst.is_dir():
                shutil.rmtree(dst)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst)

    def _write_build_info(self) -> None:
        """Write ``omnigent/_build_info.py`` into the source tree.

        Writing to the source tree (rather than directly into the
        build dir) means editable installs (``pip install -e .``,
        ``uv sync``) also get the file — they're a single
        ``build_py`` invocation against an in-place package — and
        any later non-build code path that does ``from omnigent
        import _build_info`` works without re-running the build.
        """
        # Keep generated names and types aligned with omnigent/_build_info.pyi.
        target = Path(__file__).resolve().parent / "omnigent" / "_build_info.py"
        commit = _git_sha()
        # Use repr() for the SHA so quoting is always correct, even
        # for an empty fallback. The format is deliberately minimal
        # — anything more elaborate (version strings, branch names)
        # belongs in pyproject.toml or git tags, not here.
        target.write_text(
            '"""Auto-generated at wheel build time; do not edit.\n\n'
            "This module is created by ``setup.py`` immediately before\n"
            "``build_py`` packages the wheel, and is gitignored so it\n"
            "is recreated on every build. Consumers should import it\n"
            "defensively (``try: from omnigent import _build_info``)\n"
            "because source checkouts that have never been built will\n"
            "not have it on disk.\n"
            '"""\n'
            "from __future__ import annotations\n\n"
            f"BUILD_TIME_EPOCH: int = {int(time.time())}\n"
            f"COMMIT_SHA: str = {commit!r}\n"
        )


def _git_sha() -> str:
    """Return the current Git HEAD SHA, or empty string on failure.

    Empty-string fallback is intentional: when this is run inside a
    Docker build context with no ``git`` binary, or when the build
    happens from an sdist that has no ``.git/`` directory, the field
    must still be populated with a stable string so the generated
    module remains importable. The CLI update-check treats an empty
    SHA as "no commit info available" and silently falls back to
    timestamp-only nag logic.

    :returns: 40-character full hex SHA, or ``""`` on any failure.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.SubprocessError, OSError):
        return ""
    return result.stdout.strip()


setup(cmdclass={"build_py": _GenerateBuildInfo})
