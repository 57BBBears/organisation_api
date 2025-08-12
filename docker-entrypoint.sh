#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

set -e

alembic upgrade head

if [ "$SEED_DB" = "true" ]; then
  python tests/scripts/main.py
fi

uvicorn src.main:app --host 0.0.0.0 --port 8000