from mitmproxy import ctx


def request(flow):
    flow.request.headers['User-Agent'] = 'MitmProxy'
    # 白色输出日志
    ctx.log.info(str(flow.request.headers))
    # 黄色输出
    ctx.log.warn(str(flow.request.headers))
    # 红色输出
    ctx.log.error(str(flow.request.headers))