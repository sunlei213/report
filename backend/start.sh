#!/bin/bash

# 创建必要的目录
mkdir -p instance
mkdir -p uploads

# 初始化数据库
python init_db.py

# 运行迁移
python manage.py db_upgrade

# 启动应用
python run.py 