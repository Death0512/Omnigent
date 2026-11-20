default:
    @just --list

# --- uv Python env ---

_check-uv:
    uv run --no-sync ruff --version
    uv run --no-sync pyrefly --version
    uv run --no-sync pre-commit --version

_ensure-uv:
    uv sync --extra all --group dev

# Installs the pre-commit and pre-push git hooks (see default_install_hook_types
# in .pre-commit-config.yaml). Worktrees share the main checkout's .git, so one
# install covers all of them.
_ensure-hooks: _ensure-uv
    uv run --no-sync pre-commit install

# --- omnidev Rust dev tool ---

_install-omnidev:
    cargo install --path dev/omnidev --locked --force

_check-omnidev:
    command -v omnidev >/dev/null 2>&1

_ensure-omnidev:
    command -v omnidev >/dev/null 2>&1 || just _install-omnidev

# --- Aggregate setup checks / installs ---

[group('setup')]
check: _check-uv _check-omnidev

[group('setup')]
ensure: _ensure-uv _ensure-hooks _ensure-omnidev

# --- Local dev ---

[group('dev')]
dev: _ensure-omnidev
    omnidev

[group('dev')]
crdb-up:
    docker compose -f deploy/cockroachdb/docker-compose.yml up -d --wait --wait-timeout 90
    docker compose -f deploy/cockroachdb/docker-compose.yml exec -T crdb-23-2-28 cockroach sql --insecure --execute="SET CLUSTER SETTING sql.txn.read_committed_isolation.enabled = true"

[group('dev')]
crdb-stop:
    docker compose -f deploy/cockroachdb/docker-compose.yml stop

[group('dev')]
crdb-test: crdb-up
    ./scripts/test_crdb_matrix.sh

# Destructive: stops CRDB and deletes all four persistent development volumes.
[group('dev')]
crdb-reset:
    docker compose -f deploy/cockroachdb/docker-compose.yml down --volumes

# --- Lint ---

[group('lint')]
lint: _ensure-uv
    uv run --no-sync pre-commit run

[group('lint')]
lint-all: _ensure-uv
    uv run --no-sync pre-commit run --all-files

[group('lint')]
lint-py: _ensure-uv
    uv run --no-sync ruff check .
    uv run --no-sync ruff format --check .
    uv run --no-sync pyrefly check

# Install (or reinstall) the git hooks without the rest of `just ensure`.
[group('lint')]
hooks: _ensure-hooks

[group('lint')]
typecheck-python: _ensure-uv
    uv run --no-sync pyrefly check

# --- Lockfile maintenance ---

[group('lint')]
normalize-locks: _ensure-uv
    uv run --no-sync scripts/normalize_uv_lock_registry.py uv.lock || true

# Resolve the declared dependencies through a package mirror without writing
# uv.lock; fails when a floor needs a release the mirror does not serve yet.
# Dependency groups resolve too, so a dev-only gap can fail it as well.
# No `_ensure-uv`: its `uv sync` would re-resolve and rewrite uv.lock first.
[group('lint')]
check-internal-mirror index="https://pypi-proxy.cloud.databricks.com/simple":
    uv lock --dry-run --default-index {{ index }}
