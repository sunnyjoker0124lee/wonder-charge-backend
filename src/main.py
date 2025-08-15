import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.database import db
from src.routes.task import task_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# 啟用CORS以支援跨域請求
CORS(app)

# 註冊API路由
app.register_blueprint(task_bp, url_prefix='/api')

# 初始化資料庫
with app.app_context():
    db.init_db()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """提供靜態檔案服務"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/health')
def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "database": "postgresql" if not db.use_sqlite else "sqlite"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

