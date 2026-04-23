from flask import Flask
from .routes import main_bp
import os

def create_app():
    app = Flask(__name__)
    # 設定預設配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊路由 blueprint
    app.register_blueprint(main_bp)

    return app
