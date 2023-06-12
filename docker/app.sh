#!/bin/bash

alembic upgrade head
uvicorn app.main:app --port 8080 --host 0.0.0.0