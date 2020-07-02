def response(flow):
    print(flow.request.url)
    print(flow.response.text.encode('utf-8'))