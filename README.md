# toy finance
Flask application with Redis backend for personal finance

# docker redis container setup:
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

# to check database services:
docker ps

# setup the venv
virtualenv --python=python3.7 env

# to start redis db
screen -ls to check screens
screen -S redis (screen -r redis if screen already exists)
redis-server --port 8001
[ctrl]a+d to detach screen

# to start the Controller
screen -S controller
alias python=python3
export PYTHONPATH='path/to/project'
source env/bin/activate
pip install -r requirements.txt
python bin/run_controller.py
[ctrl]a+d

# to start the application
./run_application.sh
