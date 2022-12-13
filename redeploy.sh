#!/bin/bash
tmux kill-session -t portfolio_session
source env/bin/activate
cd proyecto_musica
python manage.py runserver 0.0.0.0:8000
