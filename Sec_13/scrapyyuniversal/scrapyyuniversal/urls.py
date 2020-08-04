def china(start, end):
    for page in range(start, end + 1):
        # 根据参数组建URL
        yield "https://tech.china.com/articles/index_" + str(page) + ".html"