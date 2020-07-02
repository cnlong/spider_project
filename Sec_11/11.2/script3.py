from mitmproxy import ctx


def request(flow):
    request = flow.request
    info = ctx.log.info()
    info(request.url)
    info(str(request.headers))
    info(str(request.cookies))
    info(str(request.method))
    # 修改请求的url为新的url
    request.url = 'https://httpbin.org/get'