# toy finance
Flask application with Redis backend for personal finance

# docker redis container setup:
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

# to check database services:
docker ps

# to start the redis TaskQueue
screen -ls to check screens
screen -S redis (screen -r redis if screen already exists)
redis-server --port 8001
[ctrl]a+d to detach screen
