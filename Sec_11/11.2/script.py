def request(flow):
    # flow是HTTPflow对象，通过其request捕获当前请求的对象，修改其请求头中的属性
    flow.request.headers['User-Agent'] = 'MitmProxy'
    print(flow.request.headers)