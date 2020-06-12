"""
通过flask构建简单的web页面，用于展示代理池
成为连接代理池的api，其他用户访问这个地址即可，无需关注后端怎么连接redis数据库
"""
from flask import Flask, g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    """首页"""
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    """获取随机代理"""
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """获取代理池数量"""
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()

