"""应用入口：创建 Flask 实例并启动开发服务器"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
