# Canonical Database Migration Path

ValorAI deployment uses the checksum-enforced SQL runner:

```bash
python -m app.scripts.run_migrations
python -m app.scripts.run_migrations --verify
```

Files in this directory are immutable after application. Add changes as new,
ordered, forward-only SQL migrations. Docker `db-bootstrap` invokes this runner
before backend startup.

The legacy Alembic scaffold is not the deployment authority. It remains in the
repository only for historical inspection until a separate removal decision is
made.
