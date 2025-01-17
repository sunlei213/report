#!/bin/bash

# 拉取最新代码
git pull origin main

# 后端更新
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py db upgrade

# 前端更新
cd ../frontend
npm install
npm run build

# 重启服务
sudo systemctl restart flask_app 