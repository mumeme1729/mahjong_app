#!/bin/bash

cd /usr/src/server/app && alembic revision --autogenerate 
cd /usr/src/server/app && alembic upgrade head &&uvicorn main:app --reload --port=8000 --host=0.0.0.0