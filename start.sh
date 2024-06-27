#!/bin/bash
rm -rf /tmp/*.pid
cd app
alembic upgrade head
python -m api.main
